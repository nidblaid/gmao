from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")
