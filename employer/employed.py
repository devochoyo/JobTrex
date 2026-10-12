
from flask import jsonify
from model.model import Application, JobStatus


def employed(job_id, page, per_page):
    if job_id is None:
        return jsonify({"msg": "Job ID cannot be empty"}), 400

    if not job_id:
        return jsonify({"msg": "Job ID is required"}), 400

    job = Application.query.filter_by(
        job_id=job_id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    if not job.items:
        return jsonify({"msg": "No Employer Yet"}), 400

    return jsonify([
        {
            "job_id": i.job.id,
            "title": i.job.title,
            "applicants": i.applicant.firstname + " " + i.applicant.lastname,
            "status": i.status.value
        }
        for i in job.items
        if i.status == JobStatus.ACCEPTED
    ]), 200
