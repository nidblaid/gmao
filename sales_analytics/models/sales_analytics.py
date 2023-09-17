#-*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesAnalytics(models.Model):
    _name = 'sales.analytics'
    _description = 'Sales Analytics'

    salesperson = fields.Many2one('res.users', string='Salesperson')
    worked_days = fields.Float('Worked days')
    data_type = fields.Selection([('cold','Cold'),('fresh','Fresh')])
    seniority = fields.Integer('Seniority (M)')
    productive_days = fields.Integer('Productive days')
    leads = fields.Integer('Leads')
    dispatched_leads = fields.Integer('Dispatched Leads')
    processed_leads = fields.Integer('Processed Leads')
    processed_leads_per_day = fields.Float('PL/Day')
    quotations = fields.Integer('Quotations')
    salesorders = fields.Integer('SalesOrders')
    confirmation_rate = fields.Float('Confirmation %')
    aov = fields.Float('AOV')
    cr = fields.Float('CR')
    projected_turnover = fields.Float('PT ($)')
    delivered = fields.Integer('Delivered')
    actual_turnover = fields.Float('AT ($)')
    delivery_rate = fields.Float('Delivery %')
    assessment = fields.Integer('assessment')
    score = fields.Integer('score')
    currency_id = fields.Monetary('res.currency')
