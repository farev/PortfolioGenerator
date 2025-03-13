from sqlalchemy.orm import Session
from database import User, Portfolio
import json
import logging
from typing import Dict, Optional, List
from slugify import slugify
import uuid
from sqlalchemy import or_

logger = logging.getLogger(__name__)

class DatabaseService:
    @staticmethod
    def get_or_create_user(db: Session, user_data: Dict) -> User:
        """
        Get existing user or create a new one based on LinkedIn URL
        """
        try:
            # Try to find user by LinkedIn URL
            linkedin_url = user_data.get("linkedin")
            if linkedin_url:
                existing_user = db.query(User).filter(User.linkedin_url == linkedin_url).first()
                if existing_user:
                    logger.info(f"Found existing user with LinkedIn URL: {linkedin_url}")
                    # Update user data if needed
                    for key, value in user_data.items():
                        if key == "linkedin":
                            continue  # Skip LinkedIn as it's already matched
                        if hasattr(existing_user, key) and value:
                            setattr(existing_user, key, value)
                    db.commit()
                    return existing_user
            
            # Try to find user by GitHub URL
            github_url = user_data.get("github")
            if github_url:
                existing_user = db.query(User).filter(User.github_url == github_url).first()
                if existing_user:
                    logger.info(f"Found existing user with GitHub URL: {github_url}")
                    # Update user data if needed
                    for key, value in user_data.items():
                        if key == "github":
                            continue  # Skip GitHub as it's already matched
                        if hasattr(existing_user, key) and value:
                            setattr(existing_user, key, value)
                    db.commit()
                    return existing_user
            
            # Try to find user by email
            email = user_data.get("email")
            if email:
                existing_user = db.query(User).filter(User.email == email).first()
                if existing_user:
                    logger.info(f"Found existing user with email: {email}")
                    # Update user data if needed
                    for key, value in user_data.items():
                        if key == "email":
                            continue  # Skip email as it's already matched
                        if hasattr(existing_user, key) and value:
                            setattr(existing_user, key, value)
                    db.commit()
                    return existing_user
            
            # Create new user if not found
            new_user = User(
                name=user_data.get("name", ""),
                email=user_data.get("email"),
                linkedin_url=user_data.get("linkedin"),
                github_url=user_data.get("github"),
                skills=user_data.get("skills", "")
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(f"Created new user: {new_user.name}")
            return new_user
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error getting or creating user: {str(e)}")
            raise
    
    @staticmethod
    def save_portfolio(db: Session, user_id: int, portfolio_data: Dict) -> Portfolio:
        """
        Save a portfolio for a user
        """
        try:
            # Generate a unique slug
            name = portfolio_data.get("name", "")
            base_slug = slugify(name) if name else "portfolio"
            slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
            
            # Convert projects and experiences to JSON strings
            projects = json.dumps(portfolio_data.get("projects", []))
            experiences = json.dumps(portfolio_data.get("experiences", []))
            
            # Create new portfolio
            new_portfolio = Portfolio(
                user_id=user_id,
                slug=slug,
                html_content=portfolio_data.get("html_content", ""),
                about_me=portfolio_data.get("about_me", ""),
                interests=portfolio_data.get("interests", ""),
                projects=projects,
                experiences=experiences
            )
            db.add(new_portfolio)
            db.commit()
            db.refresh(new_portfolio)
            logger.info(f"Created new portfolio with slug: {slug}")
            return new_portfolio
            
        except Exception as e:
            db.rollback()
            logger.error(f"Error saving portfolio: {str(e)}")
            raise
    
    @staticmethod
    def get_portfolio_by_slug(db: Session, slug: str) -> Optional[Portfolio]:
        """
        Get a portfolio by its slug
        """
        try:
            portfolio = db.query(Portfolio).filter(Portfolio.slug == slug).first()
            return portfolio
        except Exception as e:
            logger.error(f"Error getting portfolio by slug: {str(e)}")
            raise
    
    @staticmethod
    def get_portfolios_by_user(db: Session, user_id: int) -> List[Portfolio]:
        """
        Get all portfolios for a user
        """
        try:
            portfolios = db.query(Portfolio).filter(Portfolio.user_id == user_id).all()
            return portfolios
        except Exception as e:
            logger.error(f"Error getting portfolios by user: {str(e)}")
            raise
    
    @staticmethod
    def find_portfolio_by_urls(db: Session, github_url: str = None, linkedin_url: str = None) -> Optional[Portfolio]:
        """
        Find a portfolio by GitHub or LinkedIn URL
        """
        try:
            # First, find users with matching URLs
            query = db.query(User)
            conditions = []
            if github_url:
                conditions.append(User.github_url == github_url)
            if linkedin_url:
                conditions.append(User.linkedin_url == linkedin_url)
            
            # Apply conditions with OR logic if both URLs are provided
            if conditions:
                if len(conditions) > 1:
                    query = query.filter(or_(*conditions))
                else:
                    query = query.filter(conditions[0])
            else:
                return None
            
            users = query.all()
            logger.info(f"Found {len(users)} users matching the URLs")
            
            if not users:
                return None
            
            # For each user, get their most recent portfolio
            for user in users:
                logger.info(f"Checking portfolios for user: {user.name} (ID: {user.id})")
                portfolio = db.query(Portfolio).filter(Portfolio.user_id == user.id).order_by(Portfolio.updated_at.desc()).first()
                if portfolio:
                    logger.info(f"Found portfolio with slug: {portfolio.slug}")
                    return portfolio
                else:
                    logger.info(f"No portfolios found for user ID: {user.id}")
            
            return None
        except Exception as e:
            logger.error(f"Error finding portfolio by URLs: {str(e)}")
            raise 