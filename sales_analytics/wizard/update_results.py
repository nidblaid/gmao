# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError
from datetime import datetime, timedelta

class UpdateResults(models.TransientModel):
    _name = 'update.results'
    _description = 'Update Results Wizard'

    # Define fields for the wizard
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    periode = fields.Selection([
        ('last_7_days', 'Derniers 7 jours'),
        ('last_30_days', 'Derniers 30 jours'),
        ('last_60_days', 'Derniers 60 jours'),
        ('last_90_days', 'Derniers 90 jours'),
        # Add more period options here if needed
    ], string='Période')
    country_id = fields.Many2one('res.country', string='Country')
    source_id = fields.Many2one('utm.source')

    # onchange method : update the start date based on the selected period
    @api.onchange('periode')
    def update_start_date(self):
        if self.periode == 'last_7_days':
            self.start_date = datetime.today().date() - timedelta(days=7)
        elif self.periode == 'last_30_days':
            self.start_date = datetime.today().date() - timedelta(days=30)
        elif self.periode == 'last_60_days':
            self.start_date = datetime.today().date() - timedelta(days=60)
        elif self.periode == 'last_90_days':
            self.start_date = datetime.today().date() - timedelta(days=90)

    # update sales analytics results
    def update_results(self):
        # Access the 'sales.analytics' and 'res.users' models
        sales_analytics = self.env['sales.analytics']
        salespersons = self.env['res.users'].search([('is_salesperson', '=', True)])

        # Iterate through each salesperson
        for salesperson in salespersons:
            # Get analytics values : 'cold' and 'fresh' data types
            cold_values = self._get_analytics_values(salesperson, 'cold')
            fresh_values = self._get_analytics_values(salesperson, 'fresh')

            # Search for existing records : 'fresh' and 'cold' data types
            sales_records_cold = sales_analytics.search([('salesperson', '=', salesperson.id), ('data_type', '=', 'cold')])
            sales_records_fresh = sales_analytics.search([('salesperson', '=', salesperson.id), ('data_type', '=', 'fresh')])

            # Update or create records : 'fresh' data type
            if sales_records_fresh:
                sales_records_fresh.write(fresh_values)
            else:
                fresh_values['salesperson'] = salesperson.id
                fresh_values['data_type'] = 'fresh'
                sales_analytics.create(fresh_values)

            # Update or create records : 'cold' data type
            if sales_records_cold:
                sales_records_cold.write(cold_values)
            else:
                cold_values['salesperson'] = salesperson.id
                cold_values['data_type'] = 'cold'
                sales_analytics.create(cold_values)

    # retrieve analytics values based on filters
    def _get_analytics_values(self, salesperson, data_type):
        # Define a domain for CRM leads
        lead_domain = [
            ('user_id', '=', salesperson.id),
            ('type', '=', 'opportunity'),
            ('stage_id.is_won', '!=', True),
            ('active', '!=', False),
        ]

        # data type filter (cold or fresh)
        if data_type == 'cold':
            lead_domain.append(('data_status', '=', 'cold'))
        elif data_type == 'fresh':
            lead_domain.append(('data_status', '=', 'fresh'))

        # source and country filters if provided
        if self.source_id:
            lead_domain.append(('source_id', '=', self.source_id.id))

        if self.country_id:
            lead_domain.append(('partner_id.country_id', '=', self.country_id.id))

        # common domain
        common_domain = [
            ('user_id', '=', salesperson.id),
            ('create_date', '>=', self.start_date),
            ('create_date', '<=', self.end_date),
        ]

        # quotations and sales orders
        quotation_domain = common_domain + [
            ('lead_type', '=', 'cold' if data_type == 'cold' else 'fresh'),
        ]

        salesorders_domain = common_domain + [
            ('state', 'in', ['sale', 'done']),
            ('lead_type', '=', 'cold' if data_type == 'cold' else 'fresh'),
        ]

        # delivered sales orders
        delivered_domain = salesorders_domain + [('delivery_status', '=', 'delivered')]

        # worked hours for the salesperson
        worked_hours = self.env['hr.attendance'].search([('employee_id.user_id.id', '=', salesperson.id),
                                                         ('check_in', '>=', self.start_date),
                                                         ('check_out', '<=', self.end_date)]).mapped('worked_hours')

        
        lead_count = self.env['crm.lead'].search_count(lead_domain)
        dispatched_count = self.env['crm.lead'].search_count([('user_id', '=', salesperson.id),
                                                             ('date_conversion', '>=', self.start_date),
                                                             ('date_conversion', '<=', self.end_date),
                                                             ('active', 'in', [True, False]),
                                                             ('data_status', '=', 'cold' if data_type == 'cold' else 'fresh')])
        processed_count = self.env['lead.processing.history'].search_count([('salesperson_id', '=', salesperson.id),
                                                                           ('date_processing', '>=', self.start_date),
                                                                           ('date_processing', '<=', self.end_date),
                                                                           ('data_status', '=', 'cold' if data_type == 'cold' else 'fresh')])
        quotations_count = self.env['sale.order'].search_count(quotation_domain)
        salesorders_count = self.env['sale.order'].search_count(salesorders_domain)
        delivered_count = self.env['sale.order'].search_count(delivered_domain)
        total_sales = self.env['sale.order'].search(salesorders_domain).mapped('total_in_company_currency')
        total_sales_delivered = self.env['sale.order'].search(delivered_domain).mapped('total_in_company_currency')
        worked_days = sum(worked_hours) / 8 if (data_type == 'fresh') else 0

        # dictionary with computed values : Above
        values = {
            'leads': lead_count,
            'worked_days': worked_days,
            'dispatched_leads': dispatched_count,
            'processed_leads': processed_count,
            'processed_leads_per_day': processed_count / worked_days if worked_days else 0,
            'data_type': data_type,
            'quotations': quotations_count,
            'salesorders': salesorders_count,
            'confirmation_rate': salesorders_count / quotations_count if quotations_count else 0,
            'aov': sum(total_sales) / salesorders_count if salesorders_count else 0,
            'cr': salesorders_count / processed_count if processed_count else 0,
            'projected_turnover': sum(total_sales),
            'delivered': delivered_count,
            'actual_turnover': sum(total_sales_delivered),
            'delivery_rate': delivered_count / salesorders_count if delivered_count else 0,
        }

        return values
