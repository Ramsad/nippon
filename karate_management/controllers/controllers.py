# -*- coding: utf-8 -*-
# from odoo import http


# class KarateManagement(http.Controller):
#     @http.route('/karate_management/karate_management/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/karate_management/karate_management/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('karate_management.listing', {
#             'root': '/karate_management/karate_management',
#             'objects': http.request.env['karate_management.karate_management'].search([]),
#         })

#     @http.route('/karate_management/karate_management/objects/<model("karate_management.karate_management"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('karate_management.object', {
#             'object': obj
#         })
