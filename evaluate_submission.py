"""Utilities for evaluating submissions against secrecy and proof requirements."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class SubmissionCriteria:
    """Represents the evaluation criteria for a submission."""

    submission_id: str
    requires_public_acknowledgment: bool
    has_proof_of_origin: bool
    has_material_impact_on_defense: bool

    def evaluate(self) -> Tuple[bool, str]:
        """Evaluate the submission according to the defined rules."""

        return evaluate_submission(
            self.submission_id,
            self.requires_public_acknowledgment,
            self.has_proof_of_origin,
            self.has_material_impact_on_defense,
        )


def evaluate_submission(
    submission_id: str,
    requires_public_acknowledgment: bool,
    has_proof_of_origin: bool,
    has_material_impact_on_defense: bool,
) -> Tuple[bool, str]:
    """Evaluate a submission using the secrecy and proof requirements.

    Args:
        submission_id: A unique identifier for the submission.
        requires_public_acknowledgment: If the originator requires public credit.
        has_proof_of_origin: If the origin of the work can be proven.
        has_material_impact_on_defense: If the work materially impacts defense systems.

    Returns:
        A tuple containing the evaluation outcome and explanatory message.
    """

    if requires_public_acknowledgment:
        return (
            False,
            (
                f"Submission '{submission_id}' REJECTED: Public acknowledgment is required, "
                "which violates the secrecy mandate."
            ),
        )

    missing_requirements = []
    if not has_proof_of_origin:
        missing_requirements.append("origin cannot be proven")
    if not has_material_impact_on_defense:
        missing_requirements.append("material impact is not demonstrated")

    if missing_requirements:
        return (
            False,
            (
                f"Submission '{submission_id}' REJECTED: Mandatory proofs are missing "
                f"({', '.join(missing_requirements)})."
            ),
        )

    return (
        True,
        (
            f"Submission '{submission_id}' ACCEPTED: All conditions (secrecy, proof of "
            "origin, and material impact) are met."
        ),
    )


if __name__ == "__main__":
    submissions = (
        SubmissionCriteria("Project_Chimera", False, True, True),
        SubmissionCriteria("Tool_Goliath", True, True, True),
        SubmissionCriteria("System_Viper", False, True, False),
        SubmissionCriteria("Concept_Phantom", False, False, False),
    )

    for criteria in submissions:
        _, decision = criteria.evaluate()
        print(decision)
