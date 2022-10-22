import PyPDF2
import re
import pandas as pd
import os
# get imported pdf file name


# creating a pdf file object
pdfFileObj = open('tycare.pdf', 'rb')

# get pdf name
pdf_name = os.path.basename(pdfFileObj.name)
pdf_name = pdf_name.replace(".pdf", "")
# print(pdf_name)

# creating a pdf reader object
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

# printing number of pages in pdf file
# print(pdfReader.numPages)

# creating a page object
# pageObj = pdfReader.getPage()
# extract whole text from all pages

text = ""
for i in range(pdfReader.numPages):
    pageObj = pdfReader.getPage(i)
    text += pageObj.extractText()

pdfFileObj.close()
# print(text)
# search a word in text case insensitive

def wellness_patient_info(text,str,status):
    # print(text)
    order_id= re.findall(r'Order ID\s(.*)', text)[0]
    #remove extra space and colon
    order_id=order_id.replace(":", "")
    order_id=order_id.strip()

    name= re.findall(r'Name\s(.*)', text)[0]
    #remove everthing after collecton date
    name=name.split("Collected On")[0]
    name=name.replace(":", "")
    name=name.strip()



    collected_on= re.findall(r'Collected On.\s(.*)', text)[0]
    collected_on=collected_on.replace(":","")
    collected_on=collected_on.strip()

    gender_and_age= re.findall(r'Gender / Age\s(.*)', text)[0]
    # print(gender_and_age)
    # find age from gender_and_age
    age = re.findall(r'\d+', gender_and_age)[0]
    
    gender=re.findall(r'[M|F].*', gender_and_age)[0]

    refer_by= re.findall(r'Ref. By\s(.*)', text)[0]
    refer_by=refer_by.replace(":","")
    refer_by=refer_by.strip()
    sample= re.findall(r'Sample\s(.*)', text)[0]
    sample=sample.replace(":","")
    sample=sample.strip()
    refer_by=refer_by.replace(sample,"")
    df = pd.DataFrame()
    df['Order ID'] = [order_id]
    df['Name'] = [name]
    df['Collected On'] = [collected_on]
    df['Age'] = [age]
    df['Gender']=[gender]
    df['Refer By'] = [refer_by]
    df['Sample'] = [sample]
    df['Report Generted'] = [str]
    df['Report Name'] = [pdf_name]
    df['Analysis Status'] = [status]
    # print(df)
    df.to_csv(f"{pdf_name}_patient_details.csv", index=False)


def tycare_patient_info(text, str, status):

    
    patient_name = re.findall(r'NAME\W*.+', text)[0]
    patient_name = patient_name.replace("NAME", "")
    age_and_gender = re.findall(r'\(.*\/[A-Z]\)', text)[0]
    # print age form age_and_gender
    age = re.findall(r'\d+', age_and_gender)[0]
    # print gender from age
    gender = re.findall(r'\/[A-Z]', age_and_gender)[0]
    gender = gender.replace("/", "")
    patient_name = patient_name.replace(age_and_gender, "")
    test_asked = re.findall(r'TEST ASKED\s(.*)', text)[0]
    patient_id = re.findall(r'PATIENTID\s(.*)', text)[0]
    patient_name = patient_name.strip()
    test_asked = test_asked.replace(":", "")
    patient_id = patient_id.replace(":", "")
    df = pd.DataFrame()
    df['Patient Name'] = [patient_name]
    df['Age'] = [age]
    df['Gender'] = [gender]
    df['Test Asked'] = [test_asked]
    df['Patient ID'] = [patient_id]
    df['Report Generted'] = [str]
    df['Report Name'] = [pdf_name]
    df['Analysis Status'] = [status]
    # add analysis report file path in analysis report column

    df['Analysis Report'] = [f"{pdf_name}_Analysis_Report.csv"]

    print(df)
    df.to_csv(f"{pdf_name}_patient_details.csv", index=False)


def hindustan_wellness(text):
    test = []
    test_method = []

    if re.search("", text):
        b = re.findall(r'^.*\w.*$', text, re.MULTILINE)
        for i in b:
            # if re.search(r'.*-\s.*', i):
            # line which contain float number and - sign
            if re.search(r'\d+\.\d+\s-\s', i):
                # if re.search(r'\d+\.\d+', i):
                # print(b[b.index(i)-1])
                # print(i)
                # print pervious index of b including first index
                test.append(b[b.index(i)-1])
                test_method.append(i)
    test_method_names = []
    results = []
    observed = []
    unit = []
    refernce = []

    for i in test_method:
        test_method_name = re.split(r'(\d+)', i, 1)[0]
        test_method_names.append(test_method_name)
        result = i.replace(test_method_name, "")
        # print(result)
        # split string by first two space occurance
        # regex to check if string contain aplhabets
        # third= re.split(r'(^.*?\s)', result, 1)[1]
        first = re.split(r'(^.*?\s)', result, 1)[1]
        # print(first)
        result=result.replace(first,"")
        print(result)
       
        if re.search(r'\d+\.\d+\s-\s\d+\.\d+', result):
            third = re.search(r'\d+\.\d+\s-\s\d+\.\d+', result).group()
            # print(third)
        # replace first and third occurance of string
        second = result.replace(first, "")

        second = second.replace(third, "")
        # print(second)
        observed.append(first)
        unit.append(second)
        refernce.append(third)

    # closing the pdf file object

    # print(test)
    df = pd.DataFrame()
    df['Test'] = test
    df['Test Method'] = test_method_names
    df['Observed'] = observed
    df['Unit'] = unit
    df['Reference'] = refernce
    # print(df)
    df.to_csv(f"{pdf_name}_Analysis_Report.csv", index=False)


def tycare(text):
    test = []
    bnews = []
    news = []
    if re.search("", text):
        b = re.findall(r'^.*\w.*$', text, re.MULTILINE)
        for i in b:
            if re.search(r'\s\s\d', i):
                # print(i)
                test.append(i)
    test_names = []
    technologys = []
    values = []
    refernces = []
    units = []

    for i in test:
        # print(i)
        unit = re.split(r'(\s\s)', i, 0)[0]
        units.append(unit)

        value = re.split(r'\s\s([+-]?([0-9]*[.])?[0-9]+)', i, 2)[1]
        values.append(value)

        new = i.replace(unit, "")
        new = new.replace(value, "")
        if "*" in new:
            new = new.replace("*", "")
        new = new.lstrip()
        news.append(new)

    for i in news:
        # print(i)
        technology = re.split(r'(^.*?\s)', i, 1)[1]
        technologys.append(technology)
        bnew = i.replace(technology, "")
        # print(bnew)
        bnews.append(bnew)

    for i in bnews:
        refernce = re.split(r'(\s[A-Z].*)', i, 1)[0]
        refernces.append(refernce)

        # print(value)
        test_name = re.split(r'(\s[A-Z].*)', i, 1)[1]
        test_names.append(test_name)
        # remove last
    df = pd.DataFrame()
    df['Test'] = test_names
    df['Technology'] = technologys
    df['Values'] = values
    df['Unit'] = units
    df['Reference'] = refernces
    print(df)

    df.to_csv(f"{pdf_name}_Analysis_Report.csv", index=False)


if __name__ == '__main__':
    # hindustan_wellness(text)
    if re.search("Hindustan Wellness", text):
        hindustan_wellness(text)
        if not os.path.exists(f"{pdf_name}_Analysis_Report.csv"):
            wellness_patient_info(text, "Hindustan Wellness", "Analysis Report Not Generated")
        else:
            wellness_patient_info(text, "Hindustan Wellness", "Analysis Report Generated")
    elif re.search("Thyrocare", text):
        tycare(text)
        if not os.path.exists(f"{pdf_name}_Analysis_Report.csv"):
            tycare_patient_info(text, "Thyrocare", "Analysis Report Not Generated")
        else:
            tycare_patient_info(text, "Thyrocare", "Analysis Report Generated")
