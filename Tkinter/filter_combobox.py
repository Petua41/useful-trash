import tkinter as tk
from tkinter import ttk
from re import search, match, IGNORECASE

class FilterCombobox(ttk.Widget):
	def __init__(self, master=None, values=[], case_sensetive=False, regexp=False, prefix=True, init_value='', all_if_empty=False, signal_function=lambda x: x, *args, **kwargs):
		'''It`s Combobx that filters it`s list of values as you type -- like Search field.
If you want FilterCombobox to pass filtered list of values to some function as you type -- pass this function to signal_function (function should recieve Python list as the only arguement).
Don`t be confused by the fact that it`s not subclass of ttk.Combobox. You can use grid and pack as it`s regular ttk.Combobox.
You can access tk.StringVar binded to this Combobx by FilterCombobx.stringvar.

Note that after FilterCombobox once created you SHOULD use FilterCombobox.new_items() instead of directly changing its combobox["values"].
Also, DON`T change other parameters on existing instance of FilterCombobox.

All parameters that FilterCombobox don`t recieve are passed into its ttk.Combobox.
You can access them as it`s just ttk.Combobox (e. g. FilterCombobox["width"] = 5 sets FilterCombobox.combobox["width"] to 5).'''
		super(FilterCombobox, self).__init__(master, "ttk::entry")
		self.orig_values = self.values = values
		self.stringvar = tk.StringVar(master, value=init_value)
		self.combobox = ttk.Combobox(master, values=self.values, textvariable=self.stringvar, *args, **kwargs)
		self.stringvar.trace_add('write', self.on_input)
		self.compare = lambda x: x
		if prefix:
			if case_sensetive:
				if regexp:		# regexp, case_sensetive, prefix
					self.compare = self.compare_regexp_case_sensetive_prefix
				else:			# case_sensetive, prefix
					self.compare = self.compare_case_sensetive_prefix
			elif regexp:		# regexp, prefix
				self.compare = self.compare_regexp_prefix
			else:				# prefix
				self.compare = self.compare_simple_prefix
		elif case_sensetive:
			if regexp:			# regexp, case_sensetive
				self.compare = self.compare_regexp_case_sensetive
			else:				# case_sensetive
				self.compare = self.compare_case_sensetive
		elif regexp:			# regexp
			self.compare = self.compare_regexp
		else:					# none
			self.compare = self.compare_simple
		self.all_if_empty = all_if_empty
		self.signal_function = signal_function
		
	def compare_simple(self, a: str, b: str):
		return a.casefold() in b.casefold()
	
	def compare_case_sensetive(self, a: str, b: str):
		return a in b
	
	def compare_regexp_case_sensetive(self, a: str, b: str):
		return search(a, b) != None
	
	def compare_regexp(self, a: str, b: str):
		return search(a, b, flags=IGNORECASE) != None
	
	def compare_simple_prefix(self, a: str, b: str):
		return b.casefold().startswith(a.casefold())
	
	def compare_case_sensetive_prefix(self, a: str, b: str):
		return b.startswith(a)
	
	def compare_regexp_prefix(self, a: str, b: str):
		return match(a, b, flags=IGNORECASE) != None
	
	def compare_regexp_case_sensetive_prefix(self, a: str, b: str):
		return match(a, b) != None
		
	def get_new_list(self, pattern: str):
		print(f'pattern = "{pattern}"')
		if len(pattern) == 0 or pattern.isspace():
			if self.all_if_empty:
				return self.orig_values
			return []
		new_list = []
		for item in self.orig_values:
			if self.compare(pattern, item):
				new_list.append(item)
		print('__'.join(new_list))
		return new_list
		
	def grid(self, *args, **kwargs):
		self.combobox.grid(*args, **kwargs)
	
	def pack(self, *args, **kwargs):
		self.combobox.pack(*args, **kwargs)
		
	def on_input(self, *args):
		new_list = self.get_new_list(self.stringvar.get())
		self.signal_function(new_list)
		self.values = new_list
		self.combobox['values'] = self.values
		
	def new_values(self, values: list):
		self.orig_values = self.values = values
		
	def __getitem__(self, key):
		return self.combobox[key]
	
	def __setitem__(self, key, value):
		self.combobox[key] = value
		
	def destroy(self, *args, **kwargs):
		self.combobox.destroy(*args, **kwargs)
		super(FilterCombobox, self).destroy(*args, **kwargs)

if __name__ == '__main__':
	root = tk.Tk()
	root['bg'] = 'white'
	values = ['First data', 'Second data', 'Third data', 'Something', 'Lorem Ipsum']
	values_labels = dict.fromkeys(values)
	def simple_sig_func(new_values: list):
		print(' '.join(new_values))
		for val in values:
			values_labels[val]['background'] = 'yellow' if val in new_values else 'white'
	fc = FilterCombobox(root, values=values, signal_function=simple_sig_func, prefix=False)
	fc.grid(row=0, column=0)
	fc['cursor'] = 'pirate'		# check that it`s supscriptable (wrieable)
	print(fc['cursor'])		# (readable)
	
	for i in range(len(values)):
		value = values[i]
		lbl = ttk.Label(root, text=value, background='white')
		lbl.grid(row=i+1, column=0, pady=10)
		values_labels[value] = lbl
	
	def close():
		fc.destroy()		# check that it`s destroyable
		root.destroy()
	
	root.protocol('WM_DELETE_WINDOW', close)
	
	root.mainloop()
