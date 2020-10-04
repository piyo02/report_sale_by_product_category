from odoo import api, fields, models

import logging
_logger = logging.getLogger(__name__)

class SaleReportByProdCat(models.TransientModel):
    _name = 'sale.report.prod.cat'

    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date(string="End Date", required=True)

    @api.multi
    def print_so_report_by_prod_cat(self):
        sale_orders = self.env['sale.order'].search([
            ('date_order', '<=', self.end_date),
            ('date_order', '>=', self.start_date),
            ('state', '=', 'sale'),
            ('invoice_status', '=', 'invoiced'),
        ],
        order='date_order asc')

        final_dict = {}

        for sale in sale_orders:
            for line in sale.order_line:
                category = line.product_id.categ_id

                qty = line.product_uom_qty
                if line.product_uom.name != line.product_id.name and line.product_uom.name == 'bigger':
                    qty = line.product_uom_qty*line.product_uom.factor_inv

                if category.name not in final_dict.keys():                    
                    final_dict[category.name] = {}
                
                data_of_cat = final_dict[category.name]

                if line.product_id.id in data_of_cat.keys():
                    data_of_prod = data_of_cat[line.product_id.id]
                    data_of_prod[2] += qty
                    data_of_prod[4] += line.price_subtotal

                else:
                    data_of_cat[line.product_id.id] = []
                    data_of_cat[line.product_id.id].append(line.product_id.default_code) #0
                    data_of_cat[line.product_id.id].append(line.product_id.name) #1
                    data_of_cat[line.product_id.id].append(qty) #2
                    data_of_cat[line.product_id.id].append(line.product_id.uom_id.name) #3
                    data_of_cat[line.product_id.id].append(line.price_subtotal) #4


        datas = {
            'ids': self.ids,
            'model': 'sale.report.prod.cat',
            'form': final_dict,
            'start_date': self.start_date,
            'end_date': self.end_date,

        }
        return self.env['report'].get_action(self,'report_sale_by_product_category.report_so_by_prod_cat', data=datas)