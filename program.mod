/*********************************************
 * OPL 12.7.0.0 Model
 * Author: Martin Galajda
 * Creation Date: Apr 11, 2018 at 8:43:40 PM
 *********************************************/
 
 int pLength=...;
 int tLength=...;
 int xTruck=...;
 int yTruck=...;
 int capacityTruck=...;
 
 range T=1..tLength;
 range P=1..pLength;
 range X=1..xTruck;
 range Y=1..yTruck;
 
 int package_x[p in P]=...;
 int package_y[p in P]=...;
 int packageWeight[p in P]=...;
 
 int incomp[1..pLength][1..pLength]=...;
 
 dvar boolean pt[p in P][t in T];
 dvar boolean pxy[p in P][1..xTruck][1..yTruck];
 dvar boolean pbl[p in P][1..xTruck][1..yTruck];
 dvar boolean usedTruck[t in T];
 dvar int highestLoadedTruck;
 
 int truckPkgPositionMap[t in T][x in X][y in Y];
 
 dvar float+ z;
 
 minimize z;
 
 subject to {
 	 
 	 // Objective function
 	 (capacityTruck * sum (t in T) usedTruck[t]) + highestLoadedTruck <= z;
 	 
 	 // Constraint 1:
 	 // Constrain every truck to carry at most "capacityTruck" kg of packages
 	 forall (t in T)
 	   sum (p in P)
 	     pt[p][t] * packageWeight[p] <= capacityTruck;
 	     
     // Constraint 2:
     // Every package is placed into exactly one truck
     forall (p in P)
       sum (t in T)
         pt[p][t] == 1;
                  
     // Constraint 3:
     // Two packages which are in the same truck cannot overlap
     forall (pOne in P)
       forall (pTwo in P: pOne != pTwo)
         forall (t in T)
           forall (x in X)
             forall (y in Y)
               // all four conditions cannot be true (maximum 3)
               // if all four conditions are true it means that
               // packages are in same truck and that they overlap on [x,y] coordinate
               // specifically: pt[pOne][t] + pt[pTwo][t] gives 2 if they are in the same truck
               pt[pOne][t] + pt[pTwo][t] + pxy[pOne][x][y] + pxy[pTwo][x][y] <= 3;
     
     // Constraint 4:
     // Packages cannot go out of the truck
     // make sure we dont go out of truck in x direction
	 forall (p in P)
	   forall (x in X)
	     forall (y in Y)
	       pbl[p][x][y] * (x + package_x[p] - 1) <= xTruck;
	
	 // make sure we dont go out of truck in y direction
	 forall (p in P)
	   forall (x in X)
	     forall (y in Y)
	       pbl[p][x][y] * (y - (package_y[p])) >=  0;
	 				
	          	 
 	 // Constraint 5:
 	 // make "highestLoadedTruck" to reflect highest loaded truck
 	 forall (t in T)
 	    sum (p in P)
 	      pt[p,t] * packageWeight[p] <= highestLoadedTruck;
 	     
 	 // Constraint 6:
 	 // Packages cannot go into same truck if incomp[pOne, pTwo] is true
 	 forall (pOne,pTwo in P: pOne != pTwo)
 	   forall (t in T)
 	     incomp[pOne][pTwo] * (pt[pOne][t] + pt[pTwo][t]) <= incomp[pOne][pTwo];
     
     // Constraint 7
     // Every package has exactly one bottom left point inside truck
     forall (p in P)
       sum (x in X)
         sum (y in Y)
           pbl[p][x][y] == 1;
     
     // Constraint 8
     // Make connection between pbl and pxy
     forall (p in P)
       forall (xOne in X)
         forall (yOne in Y)
            // either the point is not set on pxy[xOne][yOne]
            // or there is some point set to the left and bottom 1 in variable pbl (pbl[p][xTwo][yTwo])
            (
            	(1 - pxy[p][xOne][yOne])
            	+ 
            	sum (xTwo in (xOne - (package_x[p] - 1)..xOne): xTwo >= 1, 
            		yTwo in yOne..(yOne + (package_y[p] - 1)): yTwo <= yTruck) pbl[p][xTwo][yTwo] ) >= 1;
     
          
     // Constraint 9
     // Set to zero all pxy everywhere where they should not be set
	 forall (p in P)
		sum (x in X, y in Y)
		   pxy[p][x][y] == package_x[p] * package_y[p];	  	 
     
 	 // Constraint 10
 	 // Make sure that usedTruck is set to 1 when we use it
 	 forall (t in T)
 	   sum (p in P)
 	     // if usedTruck[t] is zero then we enfor every pt[p][t] to be 0 for all p
 	     pt[p][t] <= usedTruck[t] * capacityTruck;
 	 
 }
 

execute {
 	 for (var truck=1; truck <= tLength; truck++) {
 	 	for (var packageIndex=1; packageIndex <= pLength; packageIndex++) {
 	 		if (pt[packageIndex][truck] == 1) {
 	 			 for (var x=1; x <= xTruck; x++) {
 	 			 	for (var y=1; y <= yTruck; y++) {
 	 			 	 	if (pxy[packageIndex][x][y] == 1) {
 	 						truckPkgPositionMap[truck][x][y] = packageIndex;	 	 			 	 	
 	 			 	 	}
 	 			 	}	 
 	 			 }
 	 		}
 	 	}
 	 }
 	 
 	 for (var truck = 1; truck <= tLength; truck++) {
 	  	 
 	 	write("Truck ", truck);
 	 	writeln();
 	 	for (var y = 1; y <= yTruck; y++) {
 	 		for (var x = 1; x <= xTruck; x++) {
 	 			if (truckPkgPositionMap[truck][x][y] != 0 && pbl[truckPkgPositionMap[truck][x][y]][x][y] == 1) {
 	 			 	write("s", truckPkgPositionMap[truck][x][y], " ");
 	 			} else if (truckPkgPositionMap[truck][x][y] != 0) {
 					write("p", truckPkgPositionMap[truck][x][y], " ");
 				} else {
 					write("== ");				
 				}
 	 		}
 	 		writeln();
 	 	} 	 
 	 }
 }