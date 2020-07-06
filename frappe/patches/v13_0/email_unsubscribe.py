import frappe

def execute():
	email_unsubscribe = [
		{"email": "admin@gmail.com", "global_unsubscribe": 1},
		{"email": "guest@gmail.com", "global_unsubscribe": 1}
	]

	for unsubscribe in email_unsubscribe:
		if not frappe.get_all("Email Unsubscribe", filters=unsubscribe):
			doc = frappe.new_doc("Email Unsubscribe")
			doc.update(unsubscribe)
			doc.insert(ignore_permissions=True)