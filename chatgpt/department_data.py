# department_data.py

from collections import defaultdict

departments = {
    "cse": [
        "Dr. N. Bhalaji – Principal",
        "Dr. D. C. Joy Winnie Wise – Professor",
        "Dr. Lalitha R – Professor",
        "Dr. V. Anjana Devi – Professor",
        "Dr. R. Saravanan – Associate Professor",
        "Dr. Pandithurai O – Associate Professor",
        "Dr. T. Rajendran – Associate Professor",
        "Dr. Anwar Basha H. – Associate Professor",
        "Ashok M – Associate Professor",
        "C. Balaji – Associate Professor",
        "Dr. T. Nithya – Assistant Professor",
        "Dr. Ranjith Kumar M.V. – Assistant Professor",
        "C. Chairmakani – Assistant Professor",
        "AG. Noorul Julaiha – Assistant Professor",
        "B. Sriman – Assistant Professor",
        "R. Arunkumar – Assistant Professor",
        "Vijayalakshmi R. – Assistant Professor",
        "S. H. Annie Silviya – Assistant Professor",
        "S. Uma – Assistant Professor",
        "E. Venitha – Assistant Professor",
        "C.S. Somu – Assistant Professor",
        "G. Kavitha – Assistant Professor",
        "E. Pooja – Assistant Professor",
        "G. Sumathi – Assistant Professor",
        "R. Tamilselvan – Assistant Professor",
        "J. Praveen Kumar – Assistant Professor",
        "Dr. N. Indumathi – Assistant Professor",
        "Pugazhvendan I. – Professor of Practice",
        "Anantha Krishnan A. – Associate Professor of Practice",
        "Mugesh Hariharasudan – Assistant Professor of Practice"
    ],
    "ece": [
        "Dr. Sundar Rangarajan – Professor",
        "Dr. G. Nirmala Priya – Professor",
        "Dr. M. Malathi – Professor",
        "Dr. H. Sivaram – Associate Professor",
        "Dr. E. Sivanantham – Associate Professor",
        "Dr. M. Chitra – Associate Professor",
        "Dr. R. Sanmuga Sundaram – Associate Professor",
        "Dr. T. Roosefert Mohan – Associate Professor",
        "Chinnammal V – Assistant Professor",
        "Subashini V – Assistant Professor",
        "Kalyan Kumar G – Assistant Professor",
        "Kalaivani S – Assistant Professor",
        "Balaji A – Assistant Professor",
        "Malarvizhi C – Assistant Professor",
        "Vanathi A – Assistant Professor",
        "Charulatha Srinivasan – Assistant Professor",
        "Shofia Priyadharshini D. – Assistant Professor",
        "S. Sangeetha – Assistant Professor"
    ],
    "cce": [
        "Dr. C. Ganesh – Professor",
        "Dr. S. Ashok Kumar – Professor",
        "Dr. P. Sathish Kumar – Associate Professor",
        "Manimaran B. – Assistant Professor",
        "V. Sushmitha – Assistant Professor",
        "S. Bharath – Assistant Professor",
        "G. Saravanan – Assistant Professor",
        "N. Dharmaraj – Assistant Professor",
        "Vigneshvar D. – Associate Professor of Practice"
    ],
    "ee_vlsi_d&t": [
        "Dr. I. Chandra – Professor",
        "Franklin Telfer L – Assistant Professor",
        "Dr. Sheela S – Assistant Professor"
    ],
    "ec_vlsi": [
        "Dr. S. Manjula – Professor",
        "Jayamani K – Assistant Professor",
        "Monica M. – Assistant Professor",
        "Monikapreethi S.K. – Assistant Professor"
    ],
    "csbs": [
        "Dr. K. Ramkumar – Professor",
        "Dr. Subha S – Associate Professor",
        "Dr. S. Sridhar – Associate Professor",
        "M. Babu – Associate Professor",
        "Loganayaki D – Assistant Professor",
        "S. Sathiyan – Assistant Professor",
        "K. Fouzia Sulthana – Assistant Professor",
        "T. Pandiarajan – Assistant Professor",
        "R. Deepak – Assistant Professor",
        "M. Baskar – Assistant Professor",
        "K. Jayashree – Assistant Professor",
        "J. Lakshmikanth – Assistant Professor",
        "Dr. P. Kalaivani – Assistant Professor",
        "Dr. J. Maria Arockia Dass – Assistant Professor",
        "P. Jyothy – Professor of Practice"
    ],
    "ai_ds": [
        "Dr. N. Kanagavalli – Assistant Professor",
        "Dr. A. Arthi – Professor",
        "Dr. Srivenkateswaran C. – Professor",
        "Dr. M. Vivekanandan – Associate Professor",
        "Dr. B.N. Karthik – Associate Professor",
        "Dr. S. Niranjana – Assistant Professor",
        "R. Kennady – Assistant Professor",
        "S. Saranya – Assistant Professor",
        "S. Selvakumaran – Assistant Professor",
        "R. Saranya – Assistant Professor",
        "R. Kalaiyarasi – Assistant Professor",
        "V. Deepa – Assistant Professor",
        "B. Sasikala – Assistant Professor",
        "M. Bhavani – Assistant Professor",
        "S. Vaijayanthi – Assistant Professor",
        "S. Sahunthala – Assistant Professor",
        "T. Sam Paul – Assistant Professor",
        "G. Baby Saral – Assistant Professor",
        "M. Sneha – Assistant Professor",
        "Dr. Kalaiselvi S. – Assistant Professor",
        "A. Anbumani – Assistant Professor",
        "H. Hemal Babu – Assistant Professor",
        "V. Madhan – Assistant Professor",
        "Javis Jerald – Professor of Practice",
        "Nandhini – Assistant Professor of Practice",
        "K. Subashini – Assistant Professor of Practice",
        "Farzana B. – Assistant Professor of Practice"
    ],
    "cse_ai_ml": [
        "Dr. K. Regin Bose – Professor",
        "S. Shanthana – Assistant Professor",
        "F. Merlin Christo – Assistant Professor",
        "C. Gethara Gowri – Assistant Professor",
        "P. Somasundari – Assistant Professor",
        "K.G. Sara Rose – Professor of Practice"
    ],
    "mechanical": [
        "Dr. N. Pragadish – Professor",
        "Dr. Deepak Suresh – Professor",
        "Rajeswaran P. S. – Professor",
        "Dr. Rajesh Kanna S. K. – Professor",
        "Dr. M. Bakkiyaraj – Associate Professor",
        "Dr. Muthu G – Associate Professor",
        "Dr. Sai Krishnan G – Assistant Professor",
        "Dr. N. Sivashanmugam – Assistant Professor",
        "Dr. S. Bharani Kumar – Assistant Professor",
        "Srinivasan S. – Assistant Professor",
        "Vivek S – Assistant Professor"
    ]
}

# Create a reverse mapping: member to departments
member_to_departments = defaultdict(list)

for department, members in departments.items():
    for member in members:
        # Extract the name before the "–" character
        name = member.split("–")[0].strip().lower()
        member_to_departments[name].append(department)

# To handle partial matches (e.g., first name only), create an additional mapping
first_name_to_members = defaultdict(list)
for member_full_name in member_to_departments:
    first_name = member_full_name.split()[0]  # Assuming the first word is the first name
    first_name_to_members[first_name].append(member_full_name)
