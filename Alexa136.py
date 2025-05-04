import re
from PyPDF2 import PdfReader
import tkinter as tk
from tkinter import filedialog

# Lists to store data
serious_conditions = []
minor_conditions = []
medications = []
tests_investigations = []
other = []

# Criteria lists
serious_criteria = ['Cardiovascular', 'Hypertension', 'Blood transfusion', 'Anaemia', 'Chronic anaemia','High Blood Pressure', 'Coronary Artery Disease', 'Heart Failure', 'Myocardial Infarction', 'Heart Attack', 'Arrhythmia', 'Atherosclerosis', 'Valvular Heart Disease', 'Angina Pectoris',
                    'Peripheral Artery Disease', 'Implantation of cardiac pacemaker', 'Pacemaker', 'Atrial septal defect', 'Atrial fibrillation', 'Stroke', 'Ischaemic Stroke', 'Ischemic Stroke', 'Hemorrhagic Stroke', 'Transient Ischemic Attack (TIA)', 'Embolic Stroke', 'Thrombotic Stroke', 'Cryptogenic Stroke', 'Hypertensive Hemorrhage', 'Subarachnoid Hemorrhage', 'Cerebrovascular Accident', 'TIA', 'Transient Ischaemic Attack', 'Transient Ischemic Attack',
                    'Asthma', 'Obstructive Sleep Apnea', 'Pulmonary embolism', 'Thromboembolism', 'Dyspnoea', 'Breathlessness', 'Pulmonary hypertension', 'Long-term oxygen therapy', 'Chronic Obstructive Pulmonary Disease (COPD)', 'Bronchitis', 'Emphysema', 'Pneumonia', 'Interstitial Lung Disease', 'Cystic Fibrosis', 'Sleep Apnea', 'Lung Cancer', 'Allergic Rhinitis', 'Pulmonary Fibrosis', 'Tuberculosis', 'Pulmonary Hypertension', 'Sinusitis',
                    'Cancer', 'Breast Cancer', 'Lung Cancer', 'Colorectal Cancer', 'Prostate Cancer', 'Skin Cancer', 'Ovarian Cancer', 'Pancreatic Cancer', 'Leukemia', 'Lymphoma', 'Liver Cancer', 'Bladder Cancer', 'Kidney Cancer', 'Thyroid Cancer', 'Brain Cancer', 'Esophageal Cancer', 'Stomach Cancer', 'Cervical Cancer', 'Uterine Cancer', 'Testicular Cancer', 'Melanoma',
                    'Crohns disease', 'Crohns disease', 'Inflammatory Bowel Disease', 'Gastrointestinal', 'Abdominal Pain', 'Diarrhea', 'Fatigue', 'Weight Loss', 'Fistulas', 'Ulcers', 'Colon', 'Small Intestine', 'Immune System', 'Malabsorption', 'Inflammation', 'Rectum', 'Bowel Obstruction', 'Ileum', 'Autoimmune', 'Flare-up', 'Remission',
                    'Epilepsy', 'Epilepsy', 'Generalized Epilepsy', 'Focal (Partial) Epilepsy', 'Absence Seizures', 'Tonic-Clonic Seizures', 'Myoclonic Seizures', 'Atonic Seizures', 'Complex Partial Seizures', 'Simple Partial Seizures', 'Temporal Lobe Epilepsy', 'Frontal Lobe Epilepsy', 'Occipital Lobe Epilepsy', 'Parietal Lobe Epilepsy', 'Benign Rolandic Epilepsy', 'Juvenile Myoclonic Epilepsy', 'Lennox-Gastaut Syndrome', 'Dravet Syndrome',
                    'Seizures', 'Seizures', 'Aura', 'Epileptic Encephalopathy', 'Anticonvulsant', 'Neurologist', 'Anti-Epileptic Drugs (AEDs)', 'Status Epilepticus', 'Epileptogenesis', 'Epileptologist', 'Epilepsy Surgery', 'Ketogenic Diet', 'Ictal', 'Postictal', 'Prodromal', 'Neurotransmitters', 'AED Withdrawal', 'SUDEP (Sudden Unexpected Death in Epilepsy)',
                    'High cholesterol', 'High cholesterol', 'Hypercholesterolemia', 'LDL (Low-Density Lipoprotein)', 'HDL (High-Density Lipoprotein)', 'Triglycerides', 'Atherosclerosis', 'Cholesterol Plaque', 'Coronary Artery Disease', 'Arteriosclerosis', 'Dyslipidemia', 'Statins', 'Dietary Cholesterol', 'Blood Lipids', 'Cholesterol Levels', 'Cholesterol Ratio', 'Cardiovascular Risk', 'Cholesterol-lowering Medications',
                    'Diabetes', 'Diabetes', 'Diabetes Mellitus', 'Type 1 Diabetes', 'Type 2 Diabetes', 'Gestational Diabetes', 'Insulin', 'Glucose', 'Blood Sugar', 'Pancreas', 'Hyperglycemia', 'Hypoglycemia', 'HbA1c', 'Ketoacidosis', 'Diabetic Retinopathy', 'Neuropathy', 'Nephropathy', 'Foot Ulcers', 'Diabetic Ketoacidosis (DKA)', 'Polyuria', 'Polydipsia', 'Polyphagia', 'Insulin Resistance', 'Beta Cells', 'Diabetic Neuropathy', 'Diabetic Nephropathy', 'Hyperinsulinemia', 'Peripheral Artery Disease (PAD)', 'Diabetic Gastroparesis', 'Continuous Glucose Monitoring (CGM)',
                    'Blood Disorders', 'Anemia', 'Iron Deficiency Anemia', 'Vitamin Deficiency Anemia', 'Hemolytic Anemia', 'Sickle Cell Anemia', 'Aplastic Anemia', 'Thalassemia', 'Pernicious Anemia', 'Megaloblastic Anemia', 'Folate Deficiency Anemia', 'Hemorrhagic Anemia', 'Fanconi Anemia', 'Polycythemia', 'Leukemia', 'Lymphoma', 'Myeloma', 'Hemophilia', 'Thrombocytopenia', 'Von Willebrand Disease', 'Hemochromatosis', 'Deep Vein Thrombosis', 'Pulmonary Embolism', 'Septicemia', 'Leukopenia', 'Eosinophilia', 'Neutropenia', 'Polycythemia Vera', 'Disseminated Intravascular Coagulation (DIC)', 'Idiopathic Thrombocytopenic Purpura (ITP)', 'Factor V Leiden Mutation', 'Hemangioma', 'Hemosiderosis', 'Antiphospholipid Syndrome', 'Essential Thrombocythemia', 'Cooleys Anemia', 'Hemoglobinopathies', 'Factor XIII Deficiency', 'Plasma Cell Dyscrasias', 'Porphyria', 'Bernard-Soulier Syndrome', 'Hypereosinophilic Syndrome']


minor_criteria = ['Acid reflux', 'Acne', 'Allergy', 'Attention Deficit Hyperactivity Disorder', 'ADHD', 'Blindness',
                  'Benign prostatic enlargement', 'BPE', 'Broken bones', 'Fracture', 'Cataracts', 'Cataract',
                  'Carpal tunnel syndrome', 'Chicken pox', 'Cuts and abrasions',
                  'Cold' 'Influenza', 'Dyspepsia', 'Deafness', 'Diarrhoea' 'Vomiting',
                  'Eczema', 'Fungal nail infection', 'Gout', 'Gastric reflux',
                  'Glandular fever', 'Glaucoma', 'Haemorrhoids', 'Haemorrhoid', 'Hayfever',
                  'Hormone Replacement Therapy', 'HRT', 'Hysterectomy']

# Additional criteria for medications, tests, and investigations
medication_criteria = ['Aspirin', '''Statins''', 'Atorvastatin', 'Simvastatin', 'Rosuvastatin', 'Pravastatin', 'Lovastatin', 'Fluvastatin', 'Ezetimibe', 'Crestor', 'Lipitor', 'Zocor', 'Pravachol', 'Mevacor', 'Lescol', 'Vytorin', 'Zetia', 'Livalo', 'Pitavastatin',
                       '''Beta-blockers''', 'Atenolol', 'Metoprolol','Propranolol', 'Bisoprolol', 'Carvedilol', 'Nebivolol', 'Labetalol', 'Timolol', 'Nadolol', 'Sotalol',
                       '''ACE inhibitors (Angiotensin-Converting Enzyme Inhibitors)''', 'Enalapril', 'Lisinopril', 'Ramipril', 'Captopril', 'Perindopril', 'Benazepril', 'Quinapril', 'Fosinopril', 'Moexipril', 'Trandolapril',
                       '''ARBs (Angiotensin II Receptor Blockers)''', 'Losartan', 'Valsartan', 'Irbesartan', 'Candesartan', 'Olmesartan', 'Telmisartan',
                       '''Calcium channel blockers''', 'Amlodipine', 'Nifedipine', 'Diltiazem', 'Verapamil', 'Felodipine', 'Nicardipine', 'Isradipine', 'Lercanidipine', 'Nimodipine', 'Bepridil',
                       '''Diuretics''', 'Hydrochlorothiazide', 'Furosemide', 'Bumetanide', 'Torsemide', 'Spironolactone', 'Triamterene', 'Amiloride', 'Chlorthalidone', 'Indapamide', 'Metolazone',
                       'Nitroglycerin', 'Nitrostat', 'Nitro-Bid', 'Nitro-Dur', 'Nitrolingual', 'NitroMist', 'NitroQuick','Nitro-Bid IV', 'Rectiv',
                       '''Anticoagulants''','Clopidogrel', 'Plavix', 'Warfarin', 'Warfarin', 'Dabigatran', 'Rivaroxaban', 'Apixaban', 'Edoxaban',
                       '''Respiratory medications''', 'Albuterol', 'Fluticasone', 'Salmeterol', 'Ipratropium', 'Montelukast', 'Budesonide','Theophylline', 'Cromolyn', 'Formoterol', 'Tiotropium', 'Levalbuterol', 'Mometasone', 'Beclomethasone', 'Diphenhydramine',
                       '''Cancer''', 'Chemotherapy', 'Immunotherapy', 'Targeted Therapy', 'Hormone Therapy', 'Radiation Therapy', 'Stem Cell Transplantation', 'Angiogenesis Inhibitors', 'Proteasome Inhibitors', 'Tyrosine Kinase Inhibitors', 'Monoclonal Antibodies', 'Corticosteroids', 'Topoisomerase Inhibitors', 'Antimetabolites', 'Alkylating Agents', 'Platinum-based Drugs', 'Epidermal Growth Factor Receptor (EGFR) Inhibitors', 'Programmed Cell Death Protein 1 (PD-1) Inhibitors',
                       'Programmed Cell Death Ligand 1 (PD-L1) Inhibitors', 'BRAF Inhibitors', 'Imatinib', 'Paclitaxel', 'Rituximab', 'Trastuzumab', 'Tamoxifen', 'Cisplatin', 'Letrozole', 'Erlotinib', 'Fluorouracil', 'Lenalidomide', 'Bevacizumab', 'Cyclophosphamide', 'Gleevec', 'Herceptin', 'Avastin', 'Taxol', 'Arimidex', 'Revlimid', 'Rituxan', 'Tarceva',
                       '''Crohn's disease and Inflammatory Bowel Disease (IBD)''', 'Azathioprine', 'Mercaptopurine', 'Methotrexate', 'Adalimumab', 'Infliximab', 'Certolizumab pegol', 'Ustekinumab', 'Natalizumab', 'Vedolizumab', 'Mesalamine', 'Sulfasalazine',
                       '''Epilepsy&Seizures''', 'Phenytoin', 'Carbamazepine', 'Valproic Acid', 'Lamotrigine', 'Levetiracetam', 'Topiramate', 'Oxcarbazepine', 'Gabapentin', 'Pregabalin', 'Ethosuximide', 'Clonazepam', 'Clobazam', 'Lacosamide', 'Perampanel', 'Rufinamide', 'Eslicarbazepine', 'Zonisamide', 'Tiagabine', 'Vigabatrin', 'Brivaracetam', 'Diazepam', 'Lorazepam', 'Felbamate',
                       '''Diabetes''', 'Metformin', 'Glipizide', 'Glyburide', 'Gliclazide', 'Pioglitazone', 'Rosiglitazone', 'Acarbose', 'Sitagliptin', 'Linagliptin', 'Saxagliptin', 'Empagliflozin', 'Dapagliflozin', 'Canagliflozin', 'Insulin Lispro', 'Insulin Aspart', 'Insulin Glulisine', 'Insulin Glargine', 'Insulin Detemir', 'Insulin NPH', 'Humalog', 'Novolog', 'Apidra', 'Lantus', 'Levemir', 'Januvia', 'Tradjenta', 'Onglyza', 'Jardiance', 'Farxiga', 'Invokana', 'Metformin XR', 'Glucotrol', 'Glycron', 'Actos', 'Avandia', 'Precose', 'Insulin', 'Glucagon']


# Criteria lists
tests_investigations_criteria = ['Cardiovascular Conditions and Diseases', 'Electrocardiogram (ECG or EKG)', 'Echocardiogram', 'Stress Test', 'Holter Monitor', 'Cardiac Catheterization', 'Coronary Angiography', 'MRI (Magnetic Resonance Imaging)', 'CT Angiography', 'Blood Pressure Monitoring',
                                  'Respiratory Conditions and Diseases', 'Respiratory and Cardiac Services', 'Pulmonary Function Test (PFT)', 'Chest X-ray', 'CT Scan of the Chest', 'Bronchoscopy', 'Sputum Culture', 'Arterial Blood Gas (ABG) Test', 'Spirometry', 'Spirometer',
                                  'Cancer referral', 'Mammography', 'Colonoscopy', 'Pap Smear', 'Prostate-Specific Antigen (PSA) Test', 'CT Scan', 'MRI', 'Biopsy', 'Tumor Marker Tests',
                                  "Crohn's Disease and Inflammatory Bowel Disease", 'Colonoscopy', 'Flexible Sigmoidoscopy', 'Capsule Endoscopy', 'CT Enterography', 'Blood Tests (CBC, CRP)',
                                  'Epilepsy and Seizures', 'Electroencephalogram (EEG)', 'MRI (Magnetic Resonance Imaging)', 'CT Scan', 'Ambulatory EEG Monitoring',
                                  'High Cholesterol', 'Serum cholesterol level', 'total cholesterol', 'Serum cholesterol/HDL ratio', 'Serum HDL cholesterol level', 'Lipid Profile Test', 'Cholesterol Blood Test',
                                  'Diabetes', 'Haemoglobin A1c level', 'Glycated Hemoglobin (A1c) Test', 'Fasting Blood Sugar Test', 'Oral Glucose Tolerance Test (OGTT)', 'Continuous Glucose Monitoring (CGM)',
                                  'High Blood Pressure (Hypertension)', 'Blood pressure', 'Blood Pressure Measurement', 'Ambulatory Blood Pressure Monitoring', 'Electrocardiogram (ECG or EKG)', 'Blood test', 'Electroencephalogram (EEG)', 'Vagus Nerve Stimulation (VNS)', 'MRI', 'X-ray', 'CT scan', 'Colonoscopy']


# Prompt to choose the PDF file
root = tk.Tk()
root.withdraw()
pdf_file = filedialog.askopenfilename(title="Choose PDF file", filetypes=[("PDF files", "*.pdf")])

# Open PDF
pdf = PdfReader(pdf_file)

# Loop through pages
for page_num in range(len(pdf.pages)):

    # Extract text from page
    page = pdf.pages[page_num]
    page_content = page.extract_text()

    # Split text into lines
    lines = page_content.split("\n")

    # Classify each line
    for line in lines:
        # Extract date and diagnosis from the line
        date_match = re.search(r'(\d{2}-\w{3,}-\d{4})', line)
        date = date_match.group(1).strip() if date_match else None

        # Check for criteria matches
        for criteria_list, condition_list in [
            (serious_criteria, serious_conditions),
            (minor_criteria, minor_conditions),
            (medication_criteria, medications),
            (tests_investigations_criteria, tests_investigations)
        ]:
            for criteria in criteria_list:
                if re.search(r'\b{}\b'.format(re.escape(criteria)), line):
                    condition_list.append([criteria, date])
                    break  # Stop checking other criteria once a match is found

# Print results
print("\nSerious Conditions:", serious_conditions)
print("\nMinor Conditions:", minor_conditions)
print("\nMedications:", medications)
print("\nTests and Investigations:", tests_investigations)
print("\nOther:", other)
