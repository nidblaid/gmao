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
    is_pdr = fields.Boolean('is_pdr')

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    pdr_outgoing = fields.Integer(compute='_pdr_outgoing_count')
    deliveries_vehicle_count = fields.Integer(compute='_deliveries_count')
    pdr_incoming = fields.Integer(compute='_pdr_incoming_count')
    
    def get_pdr_outgoing(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pièces livrées',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('vehicle_id', '=', self.id),('is_pdr', '=', True),('state', '=', 'done'),('picking_type_id.code', '=', 'outgoing')],
            'context': "{'create': False}"
        }

    def _pdr_outgoing_count(self):
        for record in self:
            record.pdr_outgoing = self.env['stock.picking'].search_count(
                [('vehicle_id', '=', self.id),('is_pdr', '=', True),('state', '=', 'done'),('picking_type_id.code', '=', 'outgoing')])

    def get_pdr_incoming(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pièces retournées',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('vehicle_id', '=', self.id),('is_pdr', '=', True),('state', '=', 'done'),('picking_type_id.code', '=', 'incoming')],
            'context': "{'create': False}"
        }

    def _pdr_incoming_count(self):
        for record in self:
            record.pdr_incoming = self.env['stock.picking'].search_count(
                [('vehicle_id', '=', self.id),('is_pdr', '=', True),('state', '=', 'done'),('picking_type_id.code', '=', 'incoming')])
            

    def get_deliveries(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Livraisons',
            'view_mode': 'tree',
            'res_model': 'stock.picking',
            'domain': [('vehicle_id', '=', self.id),('is_pdr', '=', False),('state', '=', 'done'),('picking_type_id.code', '=', 'outgoing')],
            'context': "{'create': False}"
        }

    def _deliveries_count(self):
        for record in self:
            record.deliveries_vehicle_count = self.env['stock.picking'].search_count(
                [('vehicle_id', '=', self.id),('is_pdr', '=', False),('state', '=', 'done'),('picking_type_id.code', '=', 'outgoing')])

    
    
