# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError
from datetime import datetime, timedelta


class UpdateResults(models.TransientModel):
    _name = 'update.results'
    _description = 'Update Results Wizard'
    
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    periode = fields.Selection([
        ('last_7_days', 'Derniers 7 jours'),
        ('last_30_days', 'Derniers 30 jours'),
        ('last_60_days', 'Derniers 60 jours'),
        ('last_90_days', 'Derniers 90 jours'),
        # Ajoutez d'autres options de période ici
    ], string='Période')

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
    
    def update_results(self):
        gmao_analytics = self.env['gmao.analytics']
        vehicles = self.env['fleet.vehicle'].search([])

        for vehicle in vehicles:
            vehicle_record = gmao_analytics.search([])
            deliveries_domain = [('vehicle_id','=', vehicle.id),('state', '=', 'done'),('picking_type_id.code', '=', 'outgoing')]
            repairs_domain  = [('vehicle_id','=', vehicle.id),('state','=', 'done')]
            
            if self.start_date and end_date :
                deliveries_domain.append(('create_date', '>=', self.start_date),('create_date', '<=', self.end_date))
                repairs_domain.append(('create_date', '>=', self.start_date),('create_date', '<=', self.end_date))
                
            total_deliveries = self.env['stock.picking'].search(deliveries_domain).mapped('somme')
            total_pdr_outgoing = self.env['repair.order'].search(repairs_domain).mapped('amount_total')
        
            values = {
                'deliveries': sum(total_deliveries),
                'pdr_outgoing': sum(total_pdr_outgoing),
                
            }
            if vehicle_record:
                gmao_analytics.write(values)
            else:
                values['name'] = vehicle.id
                gmao_analytics.create(values)

        
