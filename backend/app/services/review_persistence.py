
from sqlalchemy.orm import Session

from app.models.repository import Repository
from app.models.pull_request import PullRequest
from app.models.review import Review
from app.models.finding import Finding


def save_review(
    db: Session,
    repo_data: dict,
    pr_data: dict,
    ai_review
):
    try:
        # 1. Get or create repository
        repository = (
            db.query(Repository)
            .filter(
                Repository.repo_id == repo_data["repo_id"]
            )
            .first()
        )

        if not repository:
            repository = Repository(
                repo_id=repo_data["repo_id"],
                name=repo_data["repo_name"],
                owner=repo_data["repo_owner"]
            )

            db.add(repository)
            db.flush()

        # 2. Get or create pull request
        pull_request = (
            db.query(PullRequest)
            .filter(
                PullRequest.repository_id == repository.id,
                PullRequest.pr_number == pr_data["pr_number"]
            )
            .first()
        )

        if not pull_request:
            pull_request = PullRequest(
                pr_number=pr_data["pr_number"],
                author=pr_data["author"],
                status="completed",
                repository_id=repository.id
            )

            db.add(pull_request)
            db.flush()

        else:
            pull_request.author = pr_data["author"]
            pull_request.status = "completed"

        # 3. Get or create review
        review = (
            db.query(Review)
            .filter(
                Review.pull_request_id == pull_request.id
            )
            .first()
        )

        findings = ai_review.findings

        summary = (
            f"AI code review completed. "
            f"Found {len(findings)} issues."
        )

        verdict = (
            "changes_requested" if findings else "approved"
        )

        if not review:
            review = Review(
                summary=summary,
                verdict=verdict,
                pull_request_id=pull_request.id
            )

            db.add(review)
            db.flush()

        else:
            review.summary = summary
            review.verdict = verdict

            # Remove old findings before inserting
            # the latest AI review findings.
            db.query(Finding).filter(
                Finding.review_id == review.id
            ).delete(synchronize_session=False)

        # 4. Save new findings
        for finding in findings:
            db.add(
                Finding(
                    file_path=finding.file,
                    line_number=finding.line,
                    severity=finding.severity,
                    category=finding.category,
                    explanation=finding.explanation,
                    suggestion=finding.suggestion,
                    review_id=review.id
                )
            )

        # 5. Commit everything together
        db.commit()

        logger_message = (
            f"Review saved successfully. "
            f"Repository ID: {repository.id}, "
            f"PR ID: {pull_request.id}, "
            f"Review ID: {review.id}, "
            f"Findings: {len(findings)}"
        )

        print(logger_message)

        return review.id

    except Exception:
        db.rollback()
        raise
