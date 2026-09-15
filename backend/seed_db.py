import os
import sys

# Add the backend directory to sys.path so we can import from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models.pathogen import Pathogen, PathogenFamily
from app.models.antinicrobial import Antimicrobial, AntimicrobialClass
from app.models.ckinical_rule import ClinicalRule, RuleSeverity
from app.models.cecl_count import CellCount

def seed_data():
    db = SessionLocal()

    pathogens_data = [
        {"name": "Aspergillus niger", "scientific_name": "Aspergillus niger", "family": PathogenFamily.FUNGAL, "description": "A fungus and one of the most common species of the genus Aspergillus."},
        {"name": "Bacillus subtilis", "scientific_name": "Bacillus subtilis", "family": PathogenFamily.GRAM_POSITIVE, "description": "A Gram-positive, catalase-positive bacterium, found in soil and the gastrointestinal tract of ruminants and humans."},
        {"name": "Candida albicans", "scientific_name": "Candida albicans", "family": PathogenFamily.FUNGAL, "description": "An opportunistic pathogenic yeast that is a common member of the human gut flora."},
        {"name": "Clostridium sporogenes", "scientific_name": "Clostridium sporogenes", "family": PathogenFamily.GRAM_POSITIVE, "description": "A strictly anaerobic, Gram-positive, spore-forming bacterium."},
        {"name": "Enterococcus faecalis", "scientific_name": "Enterococcus faecalis", "family": PathogenFamily.GRAM_POSITIVE, "description": "A Gram-positive, commensal bacterium inhabiting the gastrointestinal tracts of humans and other mammals."},
        {"name": "Escherichia coli", "scientific_name": "Escherichia coli", "family": PathogenFamily.GRAM_NEGATIVE, "description": "A Gram-negative, facultative anaerobic, rod-shaped bacterium commonly found in the lower intestine of warm-blooded organisms."},
        {"name": "Klebsiella pneumoniae", "scientific_name": "Klebsiella pneumoniae", "family": PathogenFamily.GRAM_NEGATIVE, "description": "A Gram-negative, non-motile, encapsulated, lactose-fermenting, facultative anaerobic, rod-shaped bacterium."},
        {"name": "Pseudomonas aeruginosa", "scientific_name": "Pseudomonas aeruginosa", "family": PathogenFamily.GRAM_NEGATIVE, "description": "A common encapsulated, Gram-negative, rod-shaped bacterium that can cause disease in plants and animals, including humans."},
        {"name": "Staphylococcus aureus", "scientific_name": "Staphylococcus aureus", "family": PathogenFamily.GRAM_POSITIVE, "description": "A Gram-positive spherically shaped bacterium, a member of the Bacillota, and is a usual member of the microbiota of the body."},
        {"name": "Streptococcus pyogenes", "scientific_name": "Streptococcus pyogenes", "family": PathogenFamily.GRAM_POSITIVE, "description": "A species of Gram-positive, aerotolerant bacterium in the genus Streptococcus."},
    ]

    pathogen_map = {}
    for p_data in pathogens_data:
        pathogen = db.query(Pathogen).filter(Pathogen.name == p_data["name"]).first()
        if not pathogen:
            pathogen = Pathogen(**p_data)
            db.add(pathogen)
            db.flush()
        pathogen_map[pathogen.name] = pathogen

    antimicrobials_data = [
        {"name": "Amoxicillin", "drug_class": AntimicrobialClass.PENICILLIN, "route_of_administration": "Oral/IV"},
        {"name": "Ciprofloxacin", "drug_class": AntimicrobialClass.FLUOROQUINOLONE, "route_of_administration": "Oral/IV"},
        {"name": "Doxycycline", "drug_class": AntimicrobialClass.TETRACYCLINE, "route_of_administration": "Oral/IV"},
        {"name": "Azithromycin", "drug_class": AntimicrobialClass.MACROLIDE, "route_of_administration": "Oral/IV"},
        {"name": "Vancomycin", "drug_class": AntimicrobialClass.GLYCOPEPTIDE, "route_of_administration": "IV"},
        {"name": "Fluconazole", "drug_class": AntimicrobialClass.OTHER, "route_of_administration": "Oral/IV"},
        {"name": "Amphotericin B", "drug_class": AntimicrobialClass.OTHER, "route_of_administration": "IV"},
        {"name": "Metronidazole", "drug_class": AntimicrobialClass.OTHER, "route_of_administration": "Oral/IV"},
        {"name": "Meropenem", "drug_class": AntimicrobialClass.CARBAPENEM, "route_of_administration": "IV"},
        {"name": "Piperacillin-Tazobactam", "drug_class": AntimicrobialClass.PENICILLIN, "route_of_administration": "IV"},
    ]

    antimicrobial_map = {}
    for a_data in antimicrobials_data:
        antimicrobial = db.query(Antimicrobial).filter(Antimicrobial.name == a_data["name"]).first()
        if not antimicrobial:
            antimicrobial = Antimicrobial(**a_data)
            db.add(antimicrobial)
            db.flush()
        antimicrobial_map[antimicrobial.name] = antimicrobial

    rules_data = [
        ("Escherichia coli", "Amoxicillin", RuleSeverity.WARNING, "E. coli often produces beta-lactamases making it resistant to amoxicillin. Consider amoxicillin-clavulanate or ciprofloxacin instead."),
        ("Escherichia coli", "Ciprofloxacin", RuleSeverity.INFO, "Susceptible. Ciprofloxacin is generally effective for E. coli UTI."),
        ("Staphylococcus aureus", "Amoxicillin", RuleSeverity.CRITICAL, "Most S. aureus produce penicillinase. Amoxicillin alone is ineffective. Use flucloxacillin or if MRSA, use Vancomycin."),
        ("Staphylococcus aureus", "Vancomycin", RuleSeverity.INFO, "Vancomycin is the drug of choice for MRSA (Methicillin-Resistant Staphylococcus aureus)."),
        ("Pseudomonas aeruginosa", "Amoxicillin", RuleSeverity.CRITICAL, "P. aeruginosa is intrinsically resistant to amoxicillin. Avoid."),
        ("Pseudomonas aeruginosa", "Ciprofloxacin", RuleSeverity.INFO, "Ciprofloxacin has anti-pseudomonal activity and is an oral option."),
        ("Pseudomonas aeruginosa", "Piperacillin-Tazobactam", RuleSeverity.INFO, "Excellent anti-pseudomonal coverage. Recommended for severe infections."),
        ("Klebsiella pneumoniae", "Amoxicillin", RuleSeverity.CRITICAL, "Klebsiella possesses chromosomal SHV-1 beta-lactamase, conferring intrinsic resistance to ampicillin and amoxicillin."),
        ("Klebsiella pneumoniae", "Meropenem", RuleSeverity.INFO, "Carbapenems are highly effective, especially for ESBL-producing Klebsiella."),
        ("Candida albicans", "Amoxicillin", RuleSeverity.CRITICAL, "Fungal pathogen. Antibacterials like Amoxicillin are completely ineffective."),
        ("Candida albicans", "Fluconazole", RuleSeverity.INFO, "Fluconazole is highly effective and the first-line treatment for most C. albicans infections."),
        ("Aspergillus niger", "Fluconazole", RuleSeverity.CRITICAL, "Aspergillus species are intrinsically resistant to fluconazole. Use Amphotericin B or Voriconazole."),
        ("Aspergillus niger", "Amphotericin B", RuleSeverity.INFO, "Amphotericin B is active against Aspergillus species."),
        ("Enterococcus faecalis", "Amoxicillin", RuleSeverity.INFO, "Amoxicillin or Ampicillin are drugs of choice for susceptible E. faecalis."),
        ("Clostridium sporogenes", "Metronidazole", RuleSeverity.INFO, "Metronidazole provides excellent anaerobic coverage for Clostridium species."),
        ("Streptococcus pyogenes", "Amoxicillin", RuleSeverity.INFO, "S. pyogenes is universally susceptible to penicillins. Amoxicillin is an excellent choice."),
        ("Streptococcus pyogenes", "Azithromycin", RuleSeverity.WARNING, "Azithromycin is an alternative for penicillin-allergic patients, but watch for macrolide resistance."),
        ("Bacillus subtilis", "Vancomycin", RuleSeverity.INFO, "Bacillus spp. are typically susceptible to Vancomycin, though infections are rare."),
    ]

    for p_name, a_name, severity, recommendation in rules_data:
        p_id = pathogen_map[p_name].id
        a_id = antimicrobial_map[a_name].id
        
        rule = db.query(ClinicalRule).filter(
            ClinicalRule.pathogen_id == p_id,
            ClinicalRule.antimicrobial_id == a_id
        ).first()
        
        if not rule:
            rule = ClinicalRule(
                name=f"{p_name} - {a_name} Rule",
                pathogen_id=p_id,
                antimicrobial_id=a_id,
                condition_expression="Detected",
                recommendation=recommendation,
                severity=severity
            )
            db.add(rule)
            
    db.commit()
    print("Database seeding completed successfully.")

if __name__ == "__main__":
    seed_data()
