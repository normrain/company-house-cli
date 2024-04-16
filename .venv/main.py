import argparse
import requests
import json
import csv
import math
import pandas
import time

BASE_URL = "https://api.company-information.service.gov.uk/"
def get_officers(name):
    officersUrl = BASE_URL + "search/officers?q=" + name
    officers = []

    officersResponse = requests.get(officersUrl,
                                    headers={"Authorization": <<api_key>>}
                                    ).json()
    officerResponseList = officersResponse.get('items')
    for officer in officerResponseList:
        officers.append(officer)

    totalOfficers = officersResponse.get('total_results')
    officersPerPage = officersResponse.get('items_per_page')
    index = officersPerPage

    while(index < totalOfficers):
        additionalOfficers = requests.get(officersUrl+"&start_index=" + str(index),
                                          headers={"Authorization": <<api_key>>}
                                          )
        if(additionalOfficers.status_code != 200):
           continue
        additionalOfficersJson = additionalOfficers.json()
        additionalOfficersList = additionalOfficersJson.get('items')
        if(additionalOfficersList is None):
            continue
        for additionalOfficer in additionalOfficersList:
            officers.append(additionalOfficer)
        index += officersPerPage

    return officers

def get_officer_appointments(officers):
    officerAppointments = []
    for officer in officers:
        officerAppointmentsResponse = requests.get(BASE_URL + officer.get('links').get('self'),
                                                headers={"Authorization": <<api_key>>}
                                                )

        if(officerAppointmentsResponse.status_code != 200):
            continue
        officerAppointmentsJson = officerAppointmentsResponse.json()
        officerAppointmentList = officerAppointmentsJson.get('items')
        if(officerAppointmentList is None):
            continue

        for officerAppointment in officerAppointmentList:
            officerAppointments.append(officerAppointment)
        totalAppointments = officerAppointmentsJson.get('total_results')
        appointmentsPerPage = officerAppointmentsJson.get('items_per_page')
        index = appointmentsPerPage
        while index < totalAppointments:
            additionalAppointments = requests.get(BASE_URL + officer.get('links').get('self') + "?start_index=" + str(index),
                                                  headers={"Authorization": <<api_key>>}
                                                  ).json()
            additionalAppointmentsList = additionalAppointments.get('items')
            if(additionalAppointmentsList is None):
                continue
            for additionalAppointment in additionalAppointmentsList:
                officerAppointments.append(additionalAppointment)
            index += appointmentsPerPage

    return officerAppointments

def get_additional_officers(appointments):
    additionalOfficers = []
    for appointment in appointments:
        company_number = appointment.get('appointed_to').get('company_number')
        additionalOfficersResponse = requests.get(BASE_URL + "company/" + company_number + "/officers/", headers={
            "Authorization": <<api_key>>}).json()
        additionalOfficersList= additionalOfficersResponse.get('items')
        if(additionalOfficersList is None):
            continue
        for additionalOfficer in additionalOfficersList:
            additionalOfficers.append(additionalOfficer)
        totalAppointments = additionalOfficersResponse.get('total_results')
        appointmentsPerPage = additionalOfficersResponse.get('items_per_page')
        index = appointmentsPerPage
        while index < totalAppointments:
            additionalOfficersResponse = requests.get(BASE_URL + "company/" + companyNumber + "/officers/?start_index=" + str(index), headers={
                "Authorization": <<api_key>>}).json()
            additionalOfficersList = additionalOfficersResponse.get('items')
            if(additionalOfficersList is None):
                continue
            for additionalOfficer in additionalOfficersList:
                additionalOfficers.append(additionalOfficer)
        time.sleep(1.7)
    return additionalOfficers

def get_filing_history(appointments):
    filingHistories = []
    for appointment in appointments:
        company_number = appointment.get('appointed_to').get('company_number')
        filingHistoryResponse = requests.get(BASE_URL + "company/" + companyNumber + "/filing-history/", headers={
            "Authorization":<<api_key>>}).json()
        filingHistoryList= filingHistoryResponse.get('items')
        if(filingHistoryList is None):
            continue
        for filingHistory in filingHistoryList:
            filingHistories.append(filingHistory)
        totalHistories = filingHistoryResponse.get('total_results')
        historiesPerPage = filingHistoryResponse.get('items_per_page')
        index = historiesPerPage
        while index < totalHistories:
            additionalFilingHistory = requests.get(BASE_URL + "company/" + companyNumber + "/filing-history/?start_index=" + str(index), headers={
                "Authorization": <<api_key>>}).json()
            additionalFilingHistoryList = additionalFilingHistory.get('items')
            if(additionalFilingHistoryList is None):
                continue
            for additionalFilingHistory in additionalFilingHistoryList:
                filingHistories.append(additionalFilingHistory)
        time.sleep(1.7)
    return filingHistories

def main():

    parser = argparse.ArgumentParser(description="A script that says hello.")
    parser.add_argument("name",nargs="*", help="The name of the officer")
    args = parser.parse_args()

    if(isinstance(args.name, list)):
        searchName = " ".join(args.name)
    else:
        searchName = args.name
    officers = get_officers(searchName)
    pandas.json_normalize(officers).to_csv("officers.csv")

    officerAppointments = get_officer_appointments(officers)
    pandas.json_normalize(officerAppointments).to_csv("officer_appointments.csv")

    #time.sleep(300)

    # additionalOfficers = get_additional_officers(officerAppointments)
    # pandas.json_normalize(officerAppointments).to_csv("additional_officers.csv")

    # filingHistory = get_filing_history(officerAppointments)
    # pandas.json_normalize(filingHistory).to_csv("filing_history.csv")

if __name__ == "__main__":
    main()