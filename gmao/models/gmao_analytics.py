#-*- coding: utf-8 -*-

from odoo import models, fields, api

class GmaoModel(models.Model):
    _name = 'gmao.analytics'
    _description = 'Gmao Analytics'

    name = fields.Char(string='Véhicule')
    pdr_outgoing = fields.Float('Pièces livrées', readonly="1")
    pdr_incoming = fields.Float('Pièces retournées', readonly="1")
    deliveries = fields.Float('Livraisons', readonly="1")
    
    

    
    
