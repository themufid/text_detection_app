import nltk
from tkinter import *
from tkinter import ttk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from tkinter import messagebox, filedialog
import fpdf

nltk.download('vader_lexicon')

class AnalysisText:
    def __init__(self):
        self.main = Tk()
        self.main.title("Text Detection")
        self.main.geometry("700x500")
        self.main.resizable(False, False)
        self.main.protocol("WM_DELETE_WINDOW", self.exit_program)
        
        self.header_frame = Frame(self.main, bg='blue', pady=10)
        self.header_frame.pack(fill='x')
        
        self.title_label = Label(self.header_frame, text="Text Detection", font=("Helvetica", 24), fg='white', bg='blue')
        self.title_label.pack()
        
        self.desc_label = Label(self.header_frame, text="Application for detecting sentiment in text", font=("Helvetica", 14), fg='white', bg='blue')
        self.desc_label.pack(pady=5)
      
        self.input_frame = Frame(self.main, padx=10, pady=10)
        self.input_frame.pack(fill='x')
        
        self.label1 = Label(self.input_frame, text="Type text here and press Enter for detection:", font=("Helvetica", 12))
        self.label1.pack()
        
        self.line = Entry(self.input_frame, width=70)
        self.line.pack(pady=5)
        self.line.bind("<Return>", self.run_analysis)
        
        self.result_table = ttk.Treeview(self.main, columns=("Type", "Percentage"), show='headings', height=5)
        self.result_table.heading("Type", text="Type")
        self.result_table.heading("Percentage", text="Percentage")
        self.result_table.column("Type", width=100)
        self.result_table.column("Percentage", width=150)
        self.result_table.pack(pady=10)
        
        self.download_button = Button(self.main, text="Download Results (PDF)", command=self.download_pdf, font=("Helvetica", 12), bg='green', fg='white')
        
        self.main.mainloop()
    
    def run_analysis(self, event=None):
        sentence = self.line.get()
        
        sid = SentimentIntensityAnalyzer()
        scores = sid.polarity_scores(sentence)
        
        self.scores = scores
        
        for i in self.result_table.get_children():
            self.result_table.delete(i)
        
        self.result_table.insert("", "end", values=("Negative", f"{self.scores['neg'] * 100:.2f}%"))
        self.result_table.insert("", "end", values=("Neutral", f"{self.scores['neu'] * 100:.2f}%"))
        self.result_table.insert("", "end", values=("Positive", f"{self.scores['pos'] * 100:.2f}%"))
        
        if self.scores['compound'] > 0.05:
            self.main.configure(background='green')
            messagebox.showinfo("Result", "Your text is positive!")
        elif self.scores['compound'] < -0.05:
            self.main.configure(background='red')
            messagebox.showinfo("Result", "Your text is negative!")
        else:
            self.main.configure(background='gray')
            messagebox.showinfo("Result", "Your text is neutral.")
        
        self.download_button.pack(pady=10)

    
    def download_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf = fpdf.FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            
            pdf.cell(0, 10, "Text Sentiment Analysis Results", ln=True)
            pdf.cell(0, 10, f"Text: {self.line.get()}", ln=True)
            pdf.cell(0, 10, "Analysis Results:", ln=True)
            
            pdf.cell(0, 10, f"Negative: {self.scores['neg'] * 100:.2f}%", ln=True)
            pdf.cell(0, 10, f"Neutral: {self.scores['neu'] * 100:.2f}%", ln=True)
            pdf.cell(0, 10, f"Positive: {self.scores['pos'] * 100:.2f}%", ln=True)

            pdf.output(file_path)
            messagebox.showinfo("Success", "Analysis results successfully downloaded as PDF.")
    
    def exit_program(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.main.destroy()

analysis_text = AnalysisText()
