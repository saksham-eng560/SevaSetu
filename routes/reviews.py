#submit reviews on the website
from fastapi import APIRouter, HTTPException , Depends
from models.review import Review
from app.database import get_session
from sqlmodel import select, Session

router_review = APIRouter(prefix="/reviews", tags=["Reviews"])

@router_review.post("/")
def submit_review(review: Review, Session: Session = Depends(get_session)):
    """
    Submit a new review.
    """
    new_review = Review.model_validate(review)
    Session.add(new_review)
    Session.commit()
    Session.refresh(new_review)
    return {"review": new_review.model_dump()}

@router_review.get("/{id}")
def get_reviews_list(id : int,Session: Session = Depends(get_session)):
    """
    Get a list of reviews for a specific service by its ID.
    """
    reviews = Session.exec(select(Review).where(Review.service_id == id)).all()
    if not reviews:
        raise HTTPException(status_code=404, detail="No reviews found for the given service ID.")
    return {"reviews": [review.model_dump() for review in reviews]}

@router_review.delete("/{id}")
def delete_review(id: int, Session: Session = Depends(get_session)):
    """
    Delete a review by its ID.
    """
    existing_review = Session.exec(select(Review).where(Review.id == id)).first()
    if not existing_review:
        raise HTTPException(status_code=404, detail="Review not found.")
    
    Session.delete(existing_review)
    Session.commit()
    return {"message": "Review deleted successfully."}
