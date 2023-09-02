from odoo import fields, models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    shipping_cost = fields.Float(string="Frais de Transport (m3)")

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")

class RepairOrder(models.Model):
    _inherit = 'repair.order'

    gmao_id = fields.Many2one('gmao.model', string="Gmao ID")
    vehicle_id = fields.Many2one('fleet.vehicle', string="Vehicle ID")

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    vehicle_id = fields.Many2one('fleet.vehicle', string="Véhicule")
    equipment_id = fields.Many2one('maintenance.equipment', string="Equipement")
    is_pdr = fields.Boolean('is_pdr')
    somme = fields.Float(string='Somme des coûts', compute='_compute_total_cost')
    shipping_cost = fields.Float(string='Frais de Transport (m3)', related='sale_id.shipping_cost')

    @api.depends('move_ids_without_package.cost')
    def _compute_total_cost(self):
        for picking in self:
            total_cost = sum(move.quantity_done for move in picking.move_ids_without_package)
            picking.somme = total_cost * shipping_cost

class StockMove(models.Model):
    _inherit = 'stock.move'

    cost = fields.Float('Cost', related='product_id.standard_price')

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
            'res_model': 'repair.order',
            'domain': [('vehicle_id', '=', self.id)],
            'context': "{'create': False}"
        }

    def _pdr_outgoing_count(self):
        for record in self:
            repairs = self.env['repair.order'].search([
                ('vehicle_id', '=', self.id)
            ])  
            costs = repairs.mapped('amount_total')
            total_cost = sum(costs)
            record.pdr_outgoing = total_cost
    
      

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

    
    
