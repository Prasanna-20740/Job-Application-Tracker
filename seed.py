from app import app, db, JobApplication

with app.app_context():
    applications = [
        JobApplication(company="TCS", role="Python Developer"),
        JobApplication(company="Infosys", role="Full Stack Developer"),
        JobApplication(company="Zoho", role="Software Developer")
    ]

    db.session.add_all(applications)
    db.session.commit()

    print("3 Job Applications Added Successfully!")