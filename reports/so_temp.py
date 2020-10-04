from odoo import api, models


class SaleReportCustomerWise(models.AbstractModel):
    _name = 'report.report_sale_by_product_category.report_so_by_prod_cat'

    @api.model
    def render_html(self, docids, data=None):
        docargs =  {
            'doc_ids': data.get('ids'),
            'doc_model': data.get('model'),
            'data': data['form'],
            'start_date': data['start_date'],
            'end_date': data['end_date'],
        }
        print "===================docargs",docargs
        return self.env['report'].render('report_sale_by_product_category.report_so_by_prod_cat', docargs)
