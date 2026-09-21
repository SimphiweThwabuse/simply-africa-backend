from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.pool import StaticPool

from app.auth.security import hash_password, verify_password
from app.config import settings


Base = declarative_base()

engine_kwargs = {"pool_pre_ping": True}
if settings.database_url.startswith("sqlite"):
    engine_kwargs["connect_args"] = {"check_same_thread": False}
    engine_kwargs["poolclass"] = StaticPool

engine = create_engine(settings.database_url, **engine_kwargs)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def init_db():
    from app.models import User
    from app.models.opportunity import Opportunity, OpportunityStage, OpportunityType

    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        default_password = "Password123!"
        demo_emails = {
            "khanya@simplycomplex.africa",
            "emaad@simplycomplex.africa",
            "zamani@simplycomplex.africa",
            "simphiwe@simplycomplex.africa",
            "siphiwe@simplycomplex.africa",
        }
        for user in db.query(User).all():
            if user.email in demo_emails:
                user.password_hash = hash_password(default_password)

        admin_user = db.query(User).filter(User.email == "elton@simplycomplex.africa").first()
        if admin_user is None:
            admin_user = db.query(User).first()

        seeded_opportunities = [
            ("Graduate Employment Pipeline", 9, OpportunityType.employment, OpportunityStage.won, 600000),
            ("Community Impact Sponsorship", 6, OpportunityType.sponsorship, OpportunityStage.active, 700000),
            ("Corporate Skills Partnership", 2, OpportunityType.employment, OpportunityStage.contacted, 250000),
            ("Women in Technology Sponsorship", 7, OpportunityType.sponsorship, OpportunityStage.lost, 200000),
        ]
        for title, organisation_id, opportunity_type, stage, value in seeded_opportunities:
            exists = db.query(Opportunity).filter(Opportunity.title == title).first()
            if exists is None and admin_user is not None:
                db.add(
                    Opportunity(
                        title=title,
                        organisation_id=organisation_id,
                        owner_id=admin_user.id,
                        opportunity_type=opportunity_type,
                        stage=stage,
                        estimated_value=value,
                        currency="ZAR",
                    )
                )
        db.commit()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()