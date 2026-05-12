from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class ExpenseApp(App):

    def build(self):

        layout = BoxLayout(
            orientation='vertical',
            padding=20,
            spacing=15
        )

        title = Label(
            text="Expense Tracker",
            font_size=28,
            size_hint=(1, 0.2)
        )

        self.category = TextInput(
            hint_text="Expense Category",
            multiline=False
        )

        self.amount = TextInput(
            hint_text="Amount",
            multiline=False,
            input_filter='float'
        )

        self.result = Label(
            text="Add Expense",
            font_size=20
        )

        btn = Button(
            text="Save Expense",
            size_hint=(1, 0.3),
            background_color=(0, 0.7, 0.3, 1)
        )

        btn.bind(on_press=self.save_expense)

        layout.add_widget(title)
        layout.add_widget(self.category)
        layout.add_widget(self.amount)
        layout.add_widget(btn)
        layout.add_widget(self.result)

        return layout

    def save_expense(self, instance):

        cat = self.category.text
        amt = self.amount.text

        self.result.text = f"Saved: {cat} - ₹{amt}"

        self.category.text = ""
        self.amount.text = ""


ExpenseApp().run()