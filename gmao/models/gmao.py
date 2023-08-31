#-*- coding: utf-8 -*-

from odoo import models, fields, api

class GmaoModel(models.Model):
    _name = 'gmao.model'
    _description = 'Gmao Model'

    name = fields.Char(string='Reference')
    intervention_type = fields.Selection([('reparation_interne','Réparation Interne'),('reparation_externe','Reparation externe'),('fabrication','Fabrication')])
    material = fields.Selection([('parc','Parc'),('material','Matériel')], string="Matériel à réparer")
    vehicule = fields.Many2one('fleet.vehicle', string="Véhicule")
    equipement = fields.Many2one('maintenance.equipment', string="Equipement")
    miles = fields.Float('Kilométrage (KM or Miles)')
    responsable = fields.Many2one('res.users', string="Responsable")

    
    
