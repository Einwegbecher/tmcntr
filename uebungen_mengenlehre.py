#!/usr/bin/env python3
"""
Skript zur Erstellung einer PDF-Datei mit Übungsaufgaben zur Mengenlehre
in der Diskreten Mathematik.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib import colors

# PDF-Konfiguration
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_LEFT = 25 * mm
MARGIN_RIGHT = 25 * mm
MARGIN_TOP = 20 * mm
MARGIN_BOTTOM = 20 * mm

# Stildefinitionen
def create_styles():
    """Erstellt benutzerdefinierte Stile für das PDF-Dokument."""
    from reportlab.lib.styles import ParagraphStyle as PS
    
    # Erstelle ein neues Stylesheet
    styles = {}
    
    # Überschrift 1
    styles['Title'] = PS(
        name='Title',
        fontSize=24,
        leading=28,
        alignment=1,  # Zentriert
        spaceAfter=20,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Überschrift 2
    styles['Heading1'] = PS(
        name='Heading1',
        fontSize=18,
        leading=22,
        spaceBefore=12,
        spaceAfter=6,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Überschrift 3
    styles['Heading2'] = PS(
        name='Heading2',
        fontSize=14,
        leading=18,
        spaceBefore=8,
        spaceAfter=4,
        textColor=colors.darkgreen,
        fontName='Helvetica-Bold'
    )
    
    # Standardtext
    styles['Normal'] = PS(
        name='Normal',
        fontSize=11,
        leading=14,
        spaceAfter=6,
        textColor=colors.black,
        fontName='Helvetica'
    )
    
    # Aufgaben-Text
    styles['Task'] = PS(
        name='Task',
        fontSize=11,
        leading=14,
        spaceAfter=12,
        textColor=colors.black,
        fontName='Helvetica',
        leftIndent=10
    )
    
    # Lösungshinweis
    styles['SolutionHint'] = PS(
        name='SolutionHint',
        fontSize=10,
        leading=13,
        spaceAfter=8,
        textColor=colors.grey,
        fontName='Helvetica-Oblique',
        leftIndent=10
    )
    
    return styles

# Übungsaufgaben zur Mengenlehre
def get_exercises():
    """Gibt eine Liste von Übungsaufgaben zur Mengenlehre zurück."""
    exercises = [
        {
            "title": "Grundlegende Mengenoperationen",
            "tasks": [
                {
                    "text": "Gegeben seien die Mengen A = {1, 2, 3, 4} und B = {3, 4, 5, 6}. "
                             "Bestimmen Sie: a) A ∪ B, b) A ∩ B, c) A \\ B, d) B \\ A, e) A × B.",
                    "hint": "Vereinigung enthält alle Elemente aus beiden Mengen, Schnitt nur gemeinsame Elemente."
                },
                {
                    "text": "Beweisen Sie die Absorptionsgesetze: A ∪ (A ∩ B) = A und A ∩ (A ∪ B) = A.",
                    "hint": "Verwenden Sie die Definitionen von Vereinigung und Schnitt sowie die logischen Äquivalenzen."
                },
                {
                    "text": "Zeigen Sie, dass für beliebige Mengen A, B und C gilt: "
                             "(A ∪ B) ∩ C = (A ∩ C) ∪ (B ∩ C).",
                    "hint": "Distributivgesetz - Beweis durch Elementargumentation."
                }
            ]
        },
        {
            "title": "Mächtigkeit von Mengen",
            "tasks": [
                {
                    "text": "Bestimmen Sie die Mächtigkeit der Potenzmenge von A = {a, b, c, d}. "
                             "Wie viele Teilmengen mit genau 2 Elementen gibt es?",
                    "hint": "Die Potenzmenge hat 2^n Elemente. Für k-Elemente-Teilmengen: Binomialkoeffizient C(n,k)."
                },
                {
                    "text": "Beweisen Sie: Eine Menge A hat genau dann endlich viele Elemente, "
                             "wenn ihre Potenzmenge endlich ist.",
                    "hint": "Indirekter Beweis: Annahme, A ist unendlich aber P(A) endlich führt zu Widerspruch."
                },
                {
                    "text": "Zeigen Sie, dass die Menge der geraden natürlichen Zahlen abzählbar unendlich ist.",
                    "hint": "Konstruieren Sie eine Bijektion zu den natürlichen Zahlen."
                }
            ]
        },
        {
            "title": "Relationen und Abbildungen",
            "tasks": [
                {
                    "text": "Gegeben sei die Relation R auf der Menge A = {1, 2, 3, 4} durch "
                             "R = {(1,1), (1,2), (2,1), (2,2), (3,3), (4,4)}. "
                             "Untersuchen Sie R auf Reflexivität, Symmetrie und Transitivität.",
                    "hint": "Überprüfen Sie die Definitionen: Reflexiv wenn alle (a,a) ∈ R, symmetrisch wenn (a,b) ∈ R ⇒ (b,a) ∈ R."
                },
                {
                    "text": "Seien A und B Mengen. Zeigen Sie, dass die Projektionen π₁: A × B → A "
                             "und π₂: A × B → B surjektiv sind.",
                    "hint": "Zu jedem a ∈ A existiert (a,b) ∈ A × B für beliebiges b ∈ B."
                },
                {
                    "text": "Beweisen Sie: Eine Funktion f: A → B ist genau dann injektiv, "
                             "wenn es eine Funktion g: B → A gibt mit g ∘ f = id_A.",
                    "hint": "g ist die sog. Linksinverse von f."
                }
            ]
        },
        {
            "title": "Äquivalenzrelationen und Partitionen",
            "tasks": [
                {
                    "text": "Auf der Menge Z der ganzen Zahlen sei die Relation R definiert durch: "
                             "a R b ⇔ 3 teilt (a - b). Zeigen Sie, dass R eine Äquivalenzrelation ist "
                             "und bestimmen Sie die Äquivalenzklassen.",
                    "hint": "Überprüfen Sie Reflexivität, Symmetrie, Transitivität. Äquivalenzklassen sind Restklassen modulo 3."
                },
                {
                    "text": "Gegeben sei eine Partition P der Menge A. Definieren Sie eine Relation R_P "
                             "durch: a R_P b ⇔ a und b liegen in derselben Teilmenge der Partition. "
                             "Zeigen Sie, dass R_P eine Äquivalenzrelation ist.",
                    "hint": "Die Partition definiert die Äquivalenzklassen."
                },
                {
                    "text": "Wie viele verschiedene Äquivalenzrelationen gibt es auf einer Menge mit 4 Elementen?",
                    "hint": "Die Anzahl entspricht der Anzahl der Partitionen (Bell-Zahlen). B₄ = 15."
                }
            ]
        },
        {
            "title": "Ordnungen und Verbände",
            "tasks": [
                {
                    "text": "Untersuchen Sie die Teilmengenrelation ⊆ auf der Potenzmenge P(A) "
                             "einer Menge A auf die Eigenschaften: reflexiv, antisymmetrisch, transitiv.",
                    "hint": "Teilmengenrelation ist eine Partialordnung."
                },
                {
                    "text": "Zeigen Sie, dass die Menge der natürlichen Zahlen N mit der "
                             "üblichen ≤-Relation ein Verband ist. Geben Sie inf und sup an.",
                    "hint": "inf(a,b) = min(a,b), sup(a,b) = max(a,b)."
                },
                {
                    "text": "Beweisen Sie: In einem Verband gilt das Idempotenzgesetz: "
                             "a ∨ a = a und a ∧ a = a.",
                    "hint": "Verwenden Sie die Verbandsaxiome."
                }
            ]
        },
        {
            "title": "Kardinalzahlen",
            "tasks": [
                {
                    "text": "Zeigen Sie, dass die Mengen N, Z und Q gleichmächtig sind.",
                    "hint": "Konstruieren Sie Bijektionen zwischen den Mengen."
                },
                {
                    "text": "Beweisen Sie den Satz von Cantor: Für jede Menge A gilt |A| < |P(A)|.",
                    "hint": "Indirekter Beweis: Annahme |A| = |P(A)| führt zu Widerspruch (Russells Antinomie)."
                },
                {
                    "text": "Zeigen Sie, dass die Menge der reellen Zahlen R überabzählbar ist.",
                    "hint": "Cantors Diagonalargument."
                }
            ]
        }
    ]
    
    return exercises

# PDF-Dokument erstellen
def create_pdf(output_path: str):
    """Erstellt das PDF-Dokument mit den Übungsaufgaben."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=MARGIN_LEFT,
        rightMargin=MARGIN_RIGHT,
        topMargin=MARGIN_TOP,
        bottomMargin=MARGIN_BOTTOM,
        title="Übungsaufgaben zur Mengenlehre",
        author="Diskrete Mathematik",
        subject="Mengenlehre Übungen"
    )
    
    styles = create_styles()
    story = []
    
    # Titel
    title_text = "<b>Übungsaufgaben zur Mengenlehre</b><br/>in der Diskreten Mathematik"
    story.append(Paragraph(title_text, styles['Title']))
    story.append(Spacer(1, 10 * mm))
    
    # Einführung
    intro = """
    Dieses Dokument enthält eine Sammlung von Übungsaufgaben zur Mengenlehre, 
    einem fundamentalen Teilgebiet der Diskreten Mathematik. Die Aufgaben decken 
    grundlegende Konzepte wie Mengenoperationen, Mächtigkeit, Relationen, 
    Äquivalenzrelationen und Ordnungen ab.
    """
    story.append(Paragraph(intro, styles['Normal']))
    story.append(Spacer(1, 15 * mm))
    
    # Übungsaufgaben durchlaufen
    exercises = get_exercises()
    
    for chapter_idx, chapter in enumerate(exercises, 1):
        # Kapitelüberschrift
        story.append(Paragraph(f"Kapitel {chapter_idx}: {chapter['title']}", styles['Heading1']))
        story.append(Spacer(1, 8 * mm))
        
        for task_idx, task in enumerate(chapter['tasks'], 1):
            # Aufgabenstellung
            task_text = f"<b>Aufgabe {chapter_idx}.{task_idx}:</b> {task['text']}"
            story.append(Paragraph(task_text, styles['Task']))
            
            # Lösungshinweis
            hint_text = f"<i>Hinweis:</i> {task['hint']}"
            story.append(Paragraph(hint_text, styles['SolutionHint']))
            
            story.append(Spacer(1, 5 * mm))
        
        # Seitenumbruch nach jedem Kapitel (außer dem letzten)
        if chapter_idx < len(exercises):
            story.append(PageBreak())
    
    # Schluss
    conclusion = """
    <b>Viel Erfolg beim Lösen der Aufgaben!</b><br/><br/>
    Diese Übungen sollen Ihnen helfen, die Konzepte der Mengenlehre besser zu verstehen 
    und anzuwenden. Für weitere Fragen und Vertiefungen wird die Konsultation 
    von Lehrbüchern zur Diskreten Mathematik empfohlen.
    """
    story.append(Spacer(1, 10 * mm))
    story.append(Paragraph(conclusion, styles['Normal']))
    
    # Dokument erstellen
    doc.build(story)
    print(f"PDF erfolgreich erstellt: {output_path}")

# Hauptprogramm
if __name__ == "__main__":
    output_pdf = "uebungen_mengenlehre.pdf"
    create_pdf(output_pdf)
