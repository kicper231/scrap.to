class Test:
    @staticmethod
    def test_action(main):

        data = [
            ["Surname", "Name", "Occupation"],
            ["Król", "Kacper", "itsquad"],
            ["Kopernik", "Mikołaj", "astronom"],
            ["Konopnicka", "Maria", "pisarka"],
            ["Karol", "Jung", "Filozof"],
            ["Juzef ", "Wybicki", "muzyk"],
            ["Andrzej", "Duda", "prezydent"],
        ]

        main.result_layout_widget.reset_result()
        main.update_preview_table(data)
        main.settings_layout_widget.my_list = data
        main.settings_layout_widget.available_fields = (
            main.settings_layout_widget.my_list[0]
        )
        main.settings_layout_widget.update_placeholder_list()
        main.settings_layout_widget.build_prompt_button.setEnabled(True)

        main.settings_layout_widget.query_text_edit.setText(
            "{Surname} {Name} {Occupation}"
        )
        main.settings_layout_widget.prompt_text_edit.setText(
            "Znajdz informacje o wieku, miejscu zamieszkania, ciekawostka o tej osobie"
        )
        main.settings_layout_widget.build_query_prompt()
