# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# MIT License. See license.txt
from __future__ import unicode_literals

import frappe, unittest
import frappe.desk.form.assign_to
from frappe.desk.listview import get_group_by_count
from frappe.automation.doctype.assignment_rule.test_assignment_rule import make_note

class TestAssign(unittest.TestCase):
	def test_assign(self):
		todo = frappe.get_doc({"doctype":"ToDo", "description": "test"}).insert()
		if not frappe.db.exists("User", "test@gmail.com"):
			frappe.get_doc({"doctype":"User", "email":"test@gmail.com", "first_name":"Test"}).insert()

		added = assign(todo, "test@gmail.com")

		self.assertTrue("test@gmail.com" in [d.owner for d in added])

		removed = frappe.desk.form.assign_to.remove(todo.doctype, todo.name, "test@gmail.com")

		# assignment is cleared
		assignments = frappe.desk.form.assign_to.get(dict(doctype = todo.doctype, name=todo.name))
		self.assertEqual(len(assignments), 0)

	def test_assignment_count(self):
		frappe.db.sql('delete from tabToDo')

		if not frappe.db.exists("User", "test_assign1@gmail.com"):
			frappe.get_doc({"doctype":"User", "email":"test_assign1@gmail.com", "first_name":"Test", "roles": [{"role": "System Manager"}]}).insert()

		if not frappe.db.exists("User", "test_assign2@gmail.com"):
			frappe.get_doc({"doctype":"User", "email":"test_assign2@gmail.com", "first_name":"Test", "roles": [{"role": "System Manager"}]}).insert()

		note = make_note()
		assign(note, "test_assign1@gmail.com")

		note = make_note(dict(public=1))
		assign(note, "test_assign2@gmail.com")

		note = make_note(dict(public=1))
		assign(note, "test_assign2@gmail.com")

		note = make_note()
		assign(note, "test_assign2@gmail.com")

		data = {d.name: d.count for d in get_group_by_count('Note', '[]', 'assigned_to')}

		self.assertTrue('test_assign1@gmail.com' in data)
		self.assertEqual(data['test_assign1@gmail.com'], 1)
		self.assertEqual(data['test_assign2@gmail.com'], 3)

		data = {d.name: d.count for d in get_group_by_count('Note', '[{"public": 1}]', 'assigned_to')}

		self.assertFalse('test_assign1@gmail.com' in data)
		self.assertEqual(data['test_assign2@gmail.com'], 2)

		frappe.db.rollback()


def assign(doc, user):
	return frappe.desk.form.assign_to.add({
		"assign_to": [user],
		"doctype": doc.doctype,
		"name": doc.name,
		"description": 'test',
	})
