
import logging
import os

import requests


logger = logging.getLogger(__name__)


class JobSearchService:

    BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"

    def search_jobs(self, keyword, location, results_per_page=5):

        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")

        if not app_id or not app_key:
            logger.error("Adzuna API credentials are missing")
            raise RuntimeError("Adzuna API credentials are not configured")

        params = {
            "app_id": app_id,
            "app_key": app_key,
            "what": keyword,
            "where": location,
            "results_per_page": results_per_page,
            "content-type": "application/json"
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            jobs = []

            for job in data.get("results", []):

                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company", {}).get("display_name"),
                    "location": job.get("location", {}).get("display_name"),
                    "salary_min": job.get("salary_min"),
                    "salary_max": job.get("salary_max"),
                    "redirect_url": job.get("redirect_url"),
                    "description": job.get("description")
                })

            logger.info(
                "Adzuna returned %d jobs for keyword=%s, location=%s",
                len(jobs),
                keyword,
                location
            )

            return jobs

        except requests.RequestException:
            logger.exception("Adzuna API request failed")
            raise


job_search_service = JobSearchService()
