from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Véhicule")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipement")

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    expenses_count = fields.Integer()

    
    
