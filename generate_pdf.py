from weasyprint import HTML
import os

def generate_hr_policy_pdf():
    html_content = """
    <html>
    <head>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: auto; padding: 20px; }
            h1 { color: #2c3e50; text-align: center; border-bottom: 2px solid #2c3e50; padding-bottom: 10px; }
            h2 { color: #e67e22; margin-top: 30px; }
            p { margin-bottom: 15px; }
            ul { margin-bottom: 15px; }
            .footer { margin-top: 50px; font-size: 0.8em; text-align: center; color: #7f8c8d; }
        </style>
    </head>
    <body>
        <h1>ACME Corp - Employee HR Policy</h1>
        
        <h2>1. Code of Conduct</h2>
        <p>All employees are expected to maintain professional behavior at all times. This includes respectful communication, punctuality, and adherence to company values.</p>
        
        <h2>2. Remote Work Policy</h2>
        <p>Employees are eligible for up to 3 days of remote work per week, subject to approval by their direct manager. Core working hours are from 10:00 AM to 4:00 PM.</p>
        
        <h2>3. Vacation and Time Off</h2>
        <p>Full-time employees accrue 20 days of paid time off per calendar year. Sick leave is provided separately and does not count towards vacation days.</p>
        
        <h2>4. Dress Code</h2>
        <p>ACME Corp follows a "Business Casual" dress code. On Fridays, "Casual Friday" is observed where jeans and company branded t-shirts are welcomed.</p>
        
        <h2>5. Professional Development</h2>
        <p>The company provides an annual stipend of $2,000 for certifications, workshops, and educational materials related to the employee's role.</p>
        
        <div class="footer">
            &copy; 2025 ACME Corp. All Rights Reserved. Confidential HR Document.
        </div>
    </body>
    </html>
    """
    
    output_filename = "hr_policy.pdf"
    print(f"Generating {output_filename}...")
    HTML(string=html_content).write_pdf(output_filename)
    print(f"Success! {output_filename} has been created at {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    generate_hr_policy_pdf()
