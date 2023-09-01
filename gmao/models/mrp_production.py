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

    expenses_vehicle_count = fields.Integer(_compute='expenses_count')
    
    def get_expenses(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Dépenses',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('vehicle_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def expenses_count(self):
        for record in self:
            record.expenses_count = self.env['stock.picking'].search_count(
                [('vehicle_id', '=', self.id)])

    
    
