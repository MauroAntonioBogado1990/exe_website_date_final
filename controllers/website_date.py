from odoo import http
from odoo.http import request

class WebsiteNewClientForm(http.Controller):

    @http.route(['/nuevo_cliente'], type='http', auth="public", website=True)
    def nuevo_cliente_form(self, **kw):
        # Buscar país Argentina
        argentina = request.env['res.country'].sudo().search([('code', '=', 'AR')], limit=1)

        # Provincias de Argentina
        states = request.env['res.country.state'].sudo().search([('country_id', '=', argentina.id)])

        # Responsabilidad ante AFIP
        afip_responsabilities = request.env['l10n_ar.afip.responsibility.type'].sudo().search([])

        return request.render('exe_website_date.template_nuevo_cliente_form', {
            'states': states,
            'afip_responsabilities': afip_responsabilities
        })

    @http.route(['/nuevo_cliente/enviar'], type='http', auth="public", website=True, csrf=False)
    def nuevo_cliente_enviar(self, **post):
        

        # if post.get('trabaja_mercaderia') == 'Sí':
        #     comment += f"A quién le compra o compraba repuestos: {post.get('origen_producto_si')}\n"
        # elif post.get('trabaja_mercaderia') == 'No':
        #     comment += f"¿Cómo conoció los productos?: {post.get('origen_producto_no')}\n"
        
        #agregado de pais
        countries = request.env['res.country'].sudo().search([], order='name ASC')

        #  Validación del CUIT
        cuit = post.get('vat', '').strip()
        #if not cuit.isdigit() or len(cuit) != 11:
        if len(cuit) != 11:    
            argentina = request.env['res.country'].sudo().search([('code', '=', 'AR')], limit=1)
            states = request.env['res.country.state'].sudo().search([('country_id', '=', argentina.id)])
            afip_responsabilities = request.env['l10n_ar.afip.responsibility.type'].sudo().search([])

            return request.render('exe_website_date.template_nuevo_cliente_form', {
                'error': "El CUIT debe tener exactamente 11 dígitos numéricos sin guiones.",
                'states': states,
                'afip_responsabilities': afip_responsabilities,
                'form_data': post
            })
        
        
        
        


        # ✅ Si el CUIT es válido, se crea el partner
        partner = request.env['res.partner'].sudo().create({
            'name': post.get('name'),
            'city': post.get('city'),
            'state_id': int(post.get('state_id')) if post.get('state_id') else False,
            #'country_id': int(post.get('country_id')) if post.get('country_id') else argentina.id,
            'country_id': 10,
            'street': post.get('street'),
            'zip': post.get('zip'),
            'mobile': post.get('mobile'),
            'phone': post.get('phone'),
            'email': post.get('email'),
            'company_name':post.get('company_name'),
            'vat': cuit,
            'l10n_ar_afip_responsibility_type_id': int(post.get('afip_id')) if post.get('afip_id') else False,
            'l10n_latam_identification_type_id': request.env['l10n_latam.identification.type'].sudo().search([('name', '=', 'CUIT')], limit=1).id,
            # Campos personalizados
            'how_met_us': post.get('how_met_us'),
            'how_met_us_other': post.get('how_met_us_other'),
            'interest_products': post.get('interest_products'),
            'how_met_us_other_products': post.get('how_met_us_other_products'),
            'client_type': post.get('client_type'),
            #'has_experience': post.get('has_experience') == 'on' or post.get('has_experience') == '1',
            'has_experience': post.get('has_experience') == '1',
            'motivation_text': post.get('motivation_text'),
            'website' : post.get('website_url'),
            # website_url': post.get('website_url'),
            'social_url': post.get('social_url'),
            'business_activity': post.get('business_activity'),
            'business_years': int(post.get('business_years')) if post.get('business_years') else False,
            'employee_count': int(post.get('employee_count')) if post.get('employee_count') else False,
            'store_count': post.get('store_count'),
            'product_categories_other': post.get('product_categories_other'),
            'text_others_products_categories': post.get('text_others_products_categories'),
            'additional_comments': post.get('additional_comments'),
            
            

        })
        
        # Cambia a contacto individual
        partner.sudo().write({'company_type': 'person'})
        
        
        

        return request.render('exe_website_date.template_nuevo_cliente_gracias')