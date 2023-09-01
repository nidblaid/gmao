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
    country_id = fields.Many2one('res.country', string='Country')
    source_id = fields.Many2one('utm.source')

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
        raise UserError(vehicles)

        for vehicle in vehicles:
            total_deliveries = self.env['stock.picking'].search(['vehicle_id','=', vehcile.id,]).mapped('somme')
        
            values = {
                'deliveries': sum(total_deliveries),
            }
            if vehicle:
                gmao_analytics.write(values)
            else:
                values['vehicle_id'] = vehicle.id
                gmao_analytics.create(values)

        
