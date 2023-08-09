import csv

class ScrapeUtil:

    @staticmethod
    def get_links(csv_files: list, output_file: str) -> list:
        temp_list = []
        for file in csv_files:
            ScrapeUtil._validate_csv_file(file)
            links = ScrapeUtil._extract_links(file)
            temp_list.extend(links)

        ScrapeUtil._write_links_to_csv(temp_list, output_file)

        return temp_list

    @staticmethod
    def _validate_csv_file(file: str) -> None:
        if not file.endswith('.csv'):
            raise ValueError("All files must be of type .csv")

    @staticmethod
    def _extract_links(file: str) -> list:
        links = []
        with open(file, 'r', newline='') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                ScrapeUtil._validate_link_format(row[0])
                links.append(row[0])
        return links

    @staticmethod
    def _validate_link_format(link: str) -> None:
        if not link.startswith('http'):
            raise ValueError("All links must start with 'http'")

    @staticmethod
    def _write_links_to_csv(links: list, output_file: str) -> None:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            for link in links:
                writer.writerow([link])
    @staticmethod
    def remove_duplicates(links: list) -> list:
        return list(set(links))