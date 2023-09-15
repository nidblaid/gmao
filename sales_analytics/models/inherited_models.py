
from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError
import datetime


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # Define custom fields for the Stock Picking model
    sale_id = fields.Many2one('sale.order', string='Sale Order')
    delivery_status = fields.Selection([
        ('shipped','Shipped'),
        ('out_for_delivery','Out for delivery'),
        ('not_delivered','Not delivered'),
        ('return','Return'),
        ('delivered','Delivered'),
    ])


class ResUsers(models.Model):
    _inherit = 'res.users'

    is_salesperson = fields.Boolean('Is Salesperson')




class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'Sale Order'

    # custom fields for the Sale Order model
    picking_ids = fields.One2many('stock.picking', 'sale_id', string='Pickings')
    total_in_company_currency = fields.Float('Total in CC', help="Total in company currency", compute='_compute_total_in_cc', store=True)
    delivery_status = fields.Selection(
        [('delivered', 'Delivered'), ('not_delivered', 'Not Delivered')],
        string='Delivery Status', compute='_compute_delivery_status', store=True
    )
    lead_type = fields.Selection([
        ('cold','Cold'),
        ('fresh','Fresh'),
    ])

    # computed field to calculate the total in company currency : (Al rayyane case)
    @api.depends('amount_total','currency_rate')
    def _compute_total_in_cc(self):
        for order in self:
            if order.amount_total != 0:
                order.total_in_company_currency = order.amount_total / order.currency_rate

    # computed field to calculate the delivery status : (Al rayyane case : studio field 'x_studio_delivery_status')
    @api.depends('picking_ids.x_studio_delivery_status')
    def _compute_delivery_status(self):
        for order in self:
            if order.delivery_count >= 1 :
                all_delivered = all(picking.x_studio_delivery_status == 'Delivered' for picking in order.picking_ids)
                if all_delivered:
                    order.delivery_status = 'delivered'
                else:
                    order.delivery_status = 'not_delivered'

    # General case : based on odoo base fields
    # @api.depends('picking_ids.state')
    # def _compute_delivery_status(self):
    #     for order in self:
    #         if order.delivery_count >= 1 :
    #             all_delivered = all(picking.state == 'done' for picking in order.picking_ids)
    #             if all_delivered:
    #                 order.delivery_status = 'delivered'
    #             else:
    #                 order.delivery_status = 'not_delivered'
    

    # Override the create method : set the lead_type based on opportunity_id
    @api.model
    def create(self, vals):
        sale_order = super(SaleOrder, self).create(vals)
        if 'opportunity_id' in vals:
            sale_order['lead_type'] = sale_order.opportunity_id.data_status
        return sale_order

# custom model for lead processing history
class LeadsProcessingHistory(models.Model):
    _name = 'lead.processing.history'
    _description = 'Lead Processing History'

    # fields for lead processing history
    salesperson_id = fields.Many2one('res.users', string="Salesperson")
    date_processing = fields.Date('Date of dispatch')
    stage_id = fields.Many2one('crm.stage', string="Stage")
    data_status = fields.Selection([
        ('cold','Cold'),
        ('fresh','Fresh'),
    ])
    team_id = fields.Many2one('crm.team', string='Sales Team')


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    
    date_processing = fields.Datetime('Processing Date')
    data_status = fields.Selection([
        ('cold','Cold'),
        ('fresh','Fresh'),
    ])

    # Override the write : log lead processing history
    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        if 'date_processing' in vals:
            lead_changes = self.env['lead.processing.history']
            for rec in self:
                if rec.date_processing:
                    lead_changes.create({
                        'date_processing': rec.date_processing,
                        'salesperson_id': rec.user_id.id,
                        'stage_id': rec.stage_id.id,
                        'team_id': rec.team_id.id,
                        'data_status' : rec.data_status,
                    })
        return res
