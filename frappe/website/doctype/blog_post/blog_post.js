// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Blog Post', {
	refresh: function(frm) {
		generate_google_search_preview(frm);
	},
	title: function(frm) {
		generate_google_search_preview(frm);
	},
	meta_description: function(frm) {
		generate_google_search_preview(frm);
	},
	blog_intro: function(frm) {
		generate_google_search_preview(frm);
	}
});

function generate_google_search_preview(frm) {
	let google_preview = frm.get_field("google_preview");
	let seo_title = (frm.doc.title).slice(0, 60);
	let seo_description =  (frm.doc.meta_description || frm.doc.blog_intro || "").slice(0, 160);
	let date = frm.doc.published_on ? new frappe.datetime.datetime(frm.doc.published_on).moment.format('ll') + ' - ' : '';
	let route_array = frm.doc.route ? frm.doc.route.split('/') : [];
	route_array.pop();

	google_preview.html(`
		<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400&display=swap" rel="stylesheet">
			<div style="font-family: Open Sans; padding: 15px; border: 1px solid #d1d8dd !important; border-radius: 6px;">
				<cite style="font-size: 14px; padding-top: 1px; line-height: 1.3; color: #202124; font-style: normal;">
					${frappe.boot.sitename}
					<span style="color: #5f6368;"> › ${route_array.join(' › ')}</span>
				</cite>
				<div style="font-size: 20px; line-height: 1.3; color: #1a0dab; padding-top: 4px; margin-bottom: 3px;">
						${ seo_title }
				</div>
				<p style="color: #545454; max-width: 48em; line-height: 1.58; font-size:14px;">
					<span style="color: #70757a;">${ date }</span> ${ seo_description }
				</p>
			</div>
	`);
}
