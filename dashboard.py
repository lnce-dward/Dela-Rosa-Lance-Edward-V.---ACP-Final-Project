def fetch_records():
        selected_date = date_var.get()
        try:
            datetime.strptime(selected_date, "%Y-%m-%d")  # Validate date format
            query = f"""
            SELECT * FROM {"ActivityTracker_TB" if record_type == "activity" else "MentalHealth_TB"}
            WHERE user_id = %s AND date = %s
            """
            self.cursor.execute(query, (self.user_id, selected_date))
            records = self.cursor.fetchall()

            # Display results
            result_text = "\n".join([str(record) for record in records]) if records else "No records found."
            result_label.configure(text=result_text)
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")

    ctk.CTkButton(
        history_window,
        text="Search",
        command=fetch_records,
        fg_color=self.custom_color,
        font=("Microsoft YaHei UI Light", 12)
    ).pack(pady=10)

    # Results display
    result_label = ctk.CTkLabel(history_window, text="", font=("Microsoft YaHei UI Light", 12), wraplength=450)
    result_label.pack(pady=10)
