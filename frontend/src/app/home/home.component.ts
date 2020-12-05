import {Component, OnInit} from '@angular/core';
import {HttpClient, HttpHeaders, HttpParams} from '@angular/common/http';
import {Router} from '@angular/router';

export interface ApartmentCleaningSchedule {
    name: string;
    position: number;
    nextCleaningTime: string;
}


@Component({
    selector: 'app-home',
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
    ELEMENT_DATA: ApartmentCleaningSchedule[] = [];

    rootURL = 'http://localhost:8080';
    displayedColumns: string[] = ['position', 'name', 'nextCleaningTime'];
    dataSource = [];

    // tslint:disable-next-line:variable-name
    constructor(private _http: HttpClient, private _router: Router) {
    }

    ngOnInit(): void {
        this.load_cleaning_schedule();
    }

    load_cleaning_schedule(): any {
        const auth = localStorage.getItem('auth');
        let headers = new HttpHeaders();
        headers = headers.set('Content-Type', 'application/json;');
        headers = headers.set('Authorization', 'Bearer ' + auth);

        let params = new HttpParams();
        params = params.append('datetime_from', '2020-09-29T15:00:00.000000');
        params = params.append('datetime_to', '2020-10-19T11:00:00.000000');
        this._http.get<any>(this.rootURL + '/api/v1/apartment-calendar', {headers, params}).subscribe(data => {
                this.map_schedule(data);
            },
            error => {
            }
        );
    }

    map_schedule(data): void {
        console.log(data);
        let rowNumber = 1;
        const rows = [];
        for (const item in data) {
            const row = {position: rowNumber, name: item, nextCleaningTime: data[item].next_cleaning_time.toString()};
            rowNumber += 1;
            rows.push(row);
        }
        this.dataSource = rows;
        console.log(this.ELEMENT_DATA);
    }

}
