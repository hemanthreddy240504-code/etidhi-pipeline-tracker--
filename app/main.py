from datetime import date, datetime
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "pipeline.db"
engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    company_name = Column(String(200), nullable=False)
    industry = Column(String(100), default="Other")
    city = Column(String(100), default="")
    website = Column(String(300), default="")
    employee_band = Column(String(50), default="")
    partner = Column(String(100), default="KOGO")
    expected_value = Column(Float, default=0)
    currency = Column(String(10), default="INR")
    stage = Column(String(50), default="Lead")
    probability = Column(Float, default=10)
    account_owner = Column(String(120), default="")
    team_members = Column(Text, default="")
    client_poc_name = Column(String(120), default="")
    client_poc_role = Column(String(120), default="")
    client_poc_email = Column(String(200), default="")
    client_poc_phone = Column(String(50), default="")
    source = Column(String(100), default="")
    expected_signup_date = Column(Date, nullable=True)
    last_contact_date = Column(Date, nullable=True)
    next_action = Column(String(300), default="")
    notes = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

Base.metadata.create_all(engine)

class CompanyIn(BaseModel):
    company_name: str
    industry: str = "Other"
    city: str = ""
    website: str = ""
    employee_band: str = ""
    partner: str = "KOGO"
    expected_value: float = 0
    currency: str = "INR"
    stage: str = "Lead"
    probability: float = 10
    account_owner: str = ""
    team_members: str = ""
    client_poc_name: str = ""
    client_poc_role: str = ""
    client_poc_email: str = ""
    client_poc_phone: str = ""
    source: str = ""
    expected_signup_date: Optional[date] = None
    last_contact_date: Optional[date] = None
    next_action: str = ""
    notes: str = ""

class CompanyOut(CompanyIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def seed(db: Session):
    if db.query(Company).count(): return
    rows = [
      dict(company_name="Aster Retail", industry="Retail", city="Hyderabad", website="https://aster.example", employee_band="500-1000", partner="KOGO", expected_value=1800000, stage="Proposal", probability=60, account_owner="Sukumar", team_members="Ananya, Rahul", client_poc_name="Meera Rao", client_poc_role="HR Head", client_poc_email="meera@aster.example", client_poc_phone="+91 90000 10001", source="Referral", expected_signup_date=date(2026,10,15), last_contact_date=date(2026,8,28), next_action="Send revised commercial proposal", notes="Interested in phased rollout across Hyderabad and Bengaluru."),
      dict(company_name="BlueOrbit Tech", industry="Technology", city="Bengaluru", partner="Contineu", expected_value=3200000, stage="Negotiation", probability=75, account_owner="Priya", team_members="Vikram", client_poc_name="Arjun Nair", client_poc_role="People Ops", client_poc_email="arjun@blueorbit.example", source="Inbound", expected_signup_date=date(2026,9,30), last_contact_date=date(2026,8,30), next_action="Finalise legal terms", notes="Strong fit; procurement review pending."),
      dict(company_name="Cedar Foods", industry="FMCG", city="Mumbai", partner="KOGO", expected_value=950000, stage="Discovery", probability=30, account_owner="Rahul", team_members="Ananya", client_poc_name="Nisha Shah", client_poc_role="Talent Lead", client_poc_email="nisha@cedar.example", source="Conference", expected_signup_date=date(2026,11,20), last_contact_date=date(2026,8,20), next_action="Schedule discovery workshop", notes="Exploring benefits and employee engagement use cases."),
      dict(company_name="Delta Logistics", industry="Logistics", city="Chennai", partner="Contineu", expected_value=2400000, stage="Proposal", probability=55, account_owner="Ananya", team_members="Rahul, Karthik", client_poc_name="Suresh Iyer", client_poc_role="CFO", client_poc_email="suresh@delta.example", source="Partner", expected_signup_date=date(2026,10,30), last_contact_date=date(2026,8,25), next_action="Confirm budget approval", notes="Needs ROI case for finance leadership."),
      dict(company_name="Evergreen Hospitals", industry="Healthcare", city="Pune", partner="KOGO", expected_value=1500000, stage="Lead", probability=10, account_owner="Priya", team_members="Karthik", client_poc_name="Dr. Kavita Menon", client_poc_role="Admin Director", client_poc_email="kavita@evergreen.example", source="Cold outreach", expected_signup_date=date(2027,1,15), last_contact_date=date(2026,8,12), next_action="Qualify budget and timeline", notes="Large workforce; early-stage conversation."),
      dict(company_name="Futura Manufacturing", industry="Manufacturing", city="Hyderabad", partner="Contineu", expected_value=4200000, stage="Negotiation", probability=80, account_owner="Sukumar", team_members="Priya, Karthik", client_poc_name="Ramesh Kumar", client_poc_role="CHRO", client_poc_email="ramesh@futura.example", source="Referral", expected_signup_date=date(2026,9,20), last_contact_date=date(2026,8,31), next_action="Executive sign-off", notes="High-value opportunity; leadership sponsor engaged."),
      dict(company_name="GreenLeaf Energy", industry="Energy", city="Delhi", partner="KOGO", expected_value=2700000, stage="Discovery", probability=35, account_owner="Karthik", team_members="Ananya", client_poc_name="Ishita Verma", client_poc_role="HRBP", client_poc_email="ishita@greenleaf.example", source="Webinar", expected_signup_date=date(2026,12,5), last_contact_date=date(2026,8,18), next_action="Share use-case deck", notes="Interested in employee rewards and retention."),
      dict(company_name="Harbor Finance", industry="Financial Services", city="Mumbai", partner="KOGO", expected_value=3600000, stage="Proposal", probability=65, account_owner="Rahul", team_members="Priya", client_poc_name="Vivek Joshi", client_poc_role="COO", client_poc_email="vivek@harbor.example", source="Referral", expected_signup_date=date(2026,10,8), last_contact_date=date(2026,8,27), next_action="Resolve security questionnaire", notes="Security review is the main blocker."),
      dict(company_name="Indigo Education", industry="Education", city="Hyderabad", partner="Contineu", expected_value=780000, stage="Qualified", probability=40, account_owner="Ananya", team_members="Rahul", client_poc_name="Lakshmi Devi", client_poc_role="Operations Head", client_poc_email="lakshmi@indigo.example", source="Inbound", expected_signup_date=date(2026,11,10), last_contact_date=date(2026,8,22), next_action="Demo analytics dashboard", notes="Wants reporting for multiple campuses."),
      dict(company_name="Jupiter Hotels", industry="Hospitality", city="Goa", partner="KOGO", expected_value=1200000, stage="Lead", probability=15, account_owner="Karthik", team_members="", client_poc_name="Neel Fernandes", client_poc_role="HR Manager", client_poc_email="neel@jupiter.example", source="Event", expected_signup_date=date(2027,1,30), last_contact_date=date(2026,8,5), next_action="Book introductory call", notes="Seasonal business; likely decision in Q4."),
      dict(company_name="Kite Mobility", industry="Mobility", city="Bengaluru", partner="Contineu", expected_value=2100000, stage="Qualified", probability=45, account_owner="Priya", team_members="Vikram, Ananya", client_poc_name="Sanjay Rao", client_poc_role="VP HR", client_poc_email="sanjay@kite.example", source="Partner", expected_signup_date=date(2026,10,25), last_contact_date=date(2026,8,29), next_action="Send pricing options", notes="Comparing annual vs pilot pricing."),
      dict(company_name="Lumen Pharma", industry="Pharma", city="Ahmedabad", partner="KOGO", expected_value=3000000, stage="Proposal", probability=60, account_owner="Sukumar", team_members="Rahul", client_poc_name="Pooja Patel", client_poc_role="HR Director", client_poc_email="pooja@lumen.example", source="Inbound", expected_signup_date=date(2026,10,18), last_contact_date=date(2026,8,26), next_action="Follow up after leadership meeting", notes="Positive business case; waiting on leadership."),
      dict(company_name="MetroBuild Infra", industry="Infrastructure", city="Chennai", partner="Contineu", expected_value=1750000, stage="Discovery", probability=30, account_owner="Rahul", team_members="Karthik", client_poc_name="Ajay Menon", client_poc_role="HR Manager", client_poc_email="ajay@metrobuild.example", source="Cold outreach", expected_signup_date=date(2026,12,15), last_contact_date=date(2026,8,10), next_action="Identify decision committee", notes="Complex stakeholder group."),
      dict(company_name="Nova Consumer", industry="Consumer Goods", city="Pune", partner="KOGO", expected_value=2300000, stage="Won", probability=100, account_owner="Priya", team_members="Ananya, Vikram", client_poc_name="Ritu Malhotra", client_poc_role="CHRO", client_poc_email="ritu@nova.example", source="Referral", expected_signup_date=date(2026,8,15), last_contact_date=date(2026,8,14), next_action="Handover to implementation", notes="Signed; included as example of post-signup handoff."),
      dict(company_name="Orbit Media", industry="Media", city="Mumbai", partner="Contineu", expected_value=1100000, stage="Lost", probability=0, account_owner="Karthik", team_members="", client_poc_name="Rahul Mehta", client_poc_role="HRBP", client_poc_email="rahul@orbit.example", source="Inbound", expected_signup_date=date(2026,8,1), last_contact_date=date(2026,7,15), next_action="Revisit in 6 months", notes="Paused due to budget freeze."),
    ]
    db.add_all([Company(**r) for r in rows]); db.commit()

app = FastAPI(title="EtiDhi Pipeline Tracker", version="1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.on_event("startup")
def startup():
    db=SessionLocal(); seed(db); db.close()

@app.get("/api/companies", response_model=list[CompanyOut])
def list_companies(search: str = "", stage: str = "", partner: str = "", owner: str = "", db: Session = Depends(get_db)):
    q=db.query(Company)
    if search:
        term=f"%{search}%"; q=q.filter((Company.company_name.ilike(term)) | (Company.client_poc_name.ilike(term)) | (Company.industry.ilike(term)))
    if stage: q=q.filter(Company.stage==stage)
    if partner: q=q.filter(Company.partner==partner)
    if owner: q=q.filter(Company.account_owner==owner)
    return q.order_by(Company.expected_value.desc()).all()

@app.post("/api/companies", response_model=CompanyOut)
def create_company(payload: CompanyIn, db: Session=Depends(get_db)):
    c=Company(**payload.model_dump()); db.add(c); db.commit(); db.refresh(c); return c

@app.put("/api/companies/{company_id}", response_model=CompanyOut)
def update_company(company_id:int, payload:CompanyIn, db:Session=Depends(get_db)):
    c=db.get(Company, company_id)
    if not c: raise HTTPException(404,"Company not found")
    for k,v in payload.model_dump().items(): setattr(c,k,v)
    db.commit(); db.refresh(c); return c

@app.delete("/api/companies/{company_id}")
def delete_company(company_id:int, db:Session=Depends(get_db)):
    c=db.get(Company, company_id)
    if not c: raise HTTPException(404,"Company not found")
    db.delete(c); db.commit(); return {"ok":True}

@app.get("/api/analytics")
def analytics(db:Session=Depends(get_db)):
    rows=db.query(Company).all()
    active=[r for r in rows if r.stage not in ("Won","Lost")]
    total=sum(r.expected_value or 0 for r in rows)
    pipeline=sum(r.expected_value or 0 for r in active)
    weighted=sum((r.expected_value or 0)*(r.probability or 0)/100 for r in active)
    won=sum(r.expected_value or 0 for r in rows if r.stage=="Won")
    by_stage={}
    by_partner={}
    by_owner={}
    by_industry={}
    monthly={}
    for r in rows:
        by_stage[r.stage]=by_stage.get(r.stage,0)+(r.expected_value or 0)
        by_partner[r.partner]=by_partner.get(r.partner,0)+(r.expected_value or 0)
        by_owner[r.account_owner]=by_owner.get(r.account_owner,0)+(r.expected_value or 0)
        by_industry[r.industry]=by_industry.get(r.industry,0)+(r.expected_value or 0)
        if r.expected_signup_date:
            key=r.expected_signup_date.strftime("%Y-%m")
            monthly[key]=monthly.get(key,0)+(r.expected_value or 0)
    today=date.today()
    overdue=[r for r in active if r.next_action and r.last_contact_date and (today-r.last_contact_date).days>14]
    return {"total_companies":len(rows),"active_companies":len(active),"total_value":total,"active_pipeline":pipeline,"weighted_pipeline":weighted,"won_value":won,"by_stage":by_stage,"by_partner":by_partner,"by_owner":by_owner,"by_industry":by_industry,"monthly":dict(sorted(monthly.items())),"stale_count":len(overdue)}

app.mount("/static", StaticFiles(directory=BASE_DIR/"static"), name="static")
@app.get("/")
def root(): return FileResponse(BASE_DIR/"static/index.html")
