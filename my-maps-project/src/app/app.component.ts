import { Component } from '@angular/core';
import { Http, Response } from '@angular/http';
import { Observable } from 'rxjs';
import 'rxjs/add/operator/toPromise';
import {Headers} from '@angular/http';
// import { MouseEvent as AGMMouseEvent } from '@agm/core';



@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.css'],
})



export class AppComponent {
  title: string = 'CraigsList House Finder';
  lat: number = 37.7749;
  lng: number = -122.4194;
  zoom: number = 10;

  url : string = 'https://craigslistmap.herokuapp.com/houses';
  data: string = 'House Results';

    constructor(private http : Http){}
public getHouses(lat,longitude){
    console.log(lat);
    console.log(longitude);
    var lat_str = new String(lat);
    var lat_param = lat_str.slice(0,6);
    var longitude_str = new String(longitude);
    var longitude_param = longitude_str.slice(1,6)

    var new_url = this.url.concat("/"+lat_param+"/"+longitude_param+"/");



 
    console.log(new_url)

    //plan b

    // "https://sfbay.craigslist.org/search/sfc/rea?query=tlc&postedToday=1&search_distance=30&postal="+str(postal)+"&max_price=600000&min_bedrooms=2&min_bathrooms=1&minSqft=900&availabilityMode=0&housing_type=6"

    this.http.get(new_url).toPromise().then((res)=>{
      console.log(res);
      this.data = res.json().slice(1,-1);

    });

}





   clickedMarker(label: string, index: number) {
    console.log(`clicked the marker: ${label || index}`)
  }
  
  mapClicked($event: any) {
    this.markers.push({
      lat: $event.coords.lat,
      lng: $event.coords.lng,
      draggable: true,
    });

    this.getHouses($event.coords.lat,$event.coords.lng);
  }
  
  markerDragEnd(m: marker, $event: any) {
    console.log('dragEnd', m, $event);
  }

markers: marker[] = [
	  // {
		 //  lat: 37.7749,
		 //  lng: -122.4194,
		 //  label: 'A',
		 //  draggable: true
	  // }
  ]
 

}

    // just an interface for type safety.
interface marker {
  lat: number;
  lng: number;
  label?: string;
  draggable: boolean;
}


