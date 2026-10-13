//This is universal CA tile set axioms. 
//Invention and design by Michael Simkin 2019. 
//Constants
epsilon_material = 0.03;
depth_factor = 0.6;
symbolR_factor = 0.7; 
sumbolH_factor = 0.4;
symbolW_factor = 0.25;

attach_w = 0.34;
attach_h = 2.2;
attach_dp = 1.7;
attach_c = 0.2; 
attach_f = 2; 
attach_m = 1.1;
c_factor = 0.7; //the slope of attachment mechanism. 1 = 45, 0 = 0. 
v = 3; // The size of additional material
R = 10; //The length of internal core
d1 = 2.4;
d2 = 3;

h_extrusion = v * depth_factor;
sH = v * sumbolH_factor;
sR = (R + 2 * v) * symbolR_factor * 0.5;
sW = (1 - symbolW_factor) * sR; 
sWcube = symbolW_factor * sR; 
sideH = v - 2 * epsilon_material; 
topH = v - epsilon_material;

function make3D_printable(part, ep)
{
    return intersection(part, cylinder({r1:R*3, r2: 0,h:-R*3}).translate([0,0,R*3 + ep]));
}

function MainAttachMale()
{
    w = attach_w;
    h = attach_h;
    c = attach_c; 
    f = attach_f; 
    ep = epsilon_material; 
    dp = attach_dp-ep;
    tr = dp - f*c; 
      //return linear_extrude({ height: 10,  );  
    var p = polygon({points:[ [0,-c*c_factor+ ep],[0,f*c-ep],[-c+ep,ep]]});
    var main_part = make3D_printable(cube([w-2*ep, dp-ep, h]), ep);
    var exp = make3D_printable(linear_extrude({ height: h - tr }, p), epsilon_material).translate([0,tr,tr])
    
    return union(exp, main_part).translate([ep,0,0]);
}

function MainAttachFemale()
{
    w = attach_w;
    h = attach_h;
    c = attach_c; 
    f = attach_f; 
    ep = 0; 
    dp = attach_dp-ep;
    tr = dp - f*c; 
      //return linear_extrude({ height: 10,  );  
    var p = polygon({points:[ [0,-c*c_factor+ep],[0,f*c-ep],[-c+ep,ep]]});
    var main_part = cube([w, dp, h]);
    var exp = make3D_printable(linear_extrude({ height: h - tr }, p), 0).translate([0,tr,tr])
    
    return union(exp, main_part).translate([ep,0,0]);
}

function AttachEmale()
{
   m  = attach_m;
   return union(MainAttachMale(), MainAttachMale().mirroredX().translate([m, 0, 0])); 
}

function AttachEfemale()
{
    m  = attach_m;
    h = attach_h;
    dp = attach_dp;
    w = attach_w;
    
    return difference(union(cube([m, dp, h]), MainAttachFemale(), MainAttachFemale().mirroredX().translate([m, 0, 0])),cube([m, dp, 2*h]).rotateX(-45)); 
}


function AttachS()
{
    var mr = union(AttachEmale().translate([0,0,-attach_h]),AttachEmale().translate([0,0,-attach_h]).mirroredZ());
    return mr.rotateX(90).translate([-attach_m/2,0,0]);
}

function AttachF()
{
    var mr = union(AttachEfemale().translate([0,0,-attach_h]),AttachEfemale().translate([0,0,-attach_h]).mirroredZ());
    return mr.rotateX(90).translate([-attach_m/2,0,0]);
}


function Attach(ep)
{
    
    if(ep === 0)
    {
         return union(AttachS().translate([d2, 0, 0]), 
        AttachS().translate([0, d1, 0]), 
        AttachS().translate([-d2, 0, 0]),
        AttachS().translate([0, -d1, 0]));
    }
    else
    {
        return union(AttachF().translate([d2, 0, 0]), 
        AttachF().translate([0, d1, 0]), 
        AttachF().translate([-d2, 0, 0]),
        AttachF().translate([0, -d1, 0]));
    }
    
}

function Draw0(ep)
{
   l = (sR - sW)/2 + ep; 
   u = (sR + sW)/2; 
   
   return union(rotate_extrude( polygon({points:[ [u-l,0],[u+l,0],[u,l]]}) ).translate([0,0,sH+ep]),
    difference(cylinder({r:(sR + ep), h:(sH + ep)}), cylinder({r:(sW - ep), h:(sH + ep)})));
    
}

function DrawLine(ep)
{
   sw2 = sWcube / 2;

   var p = polygon({points:[ [-sw2-ep,0],[sw2+ep,0],[0,sw2+ep]]});
   var exp = linear_extrude({ height: 2*sR }, p).translate([0,sH+ep,-sR-ep]);
   
   return union(cube([2*sR+2*ep, sWcube + 2 * ep, sH+ep]).translate([-sR-ep, -(sWcube)/2-ep, 0]),
                 exp.rotateX(90).rotateZ(90));
}

function DrawPlus(ep)
{
    return union(DrawLine(ep).rotateZ(90), DrawLine(ep));
}

function DrawPlus0(ep)
{
    return union(DrawPlus(ep), Draw0(ep));
}

function AttachSide(ep)
{
    return union(
        AttachS().translate([-d1,-d1,0]),
        AttachS().translate([-d1,d1,0]),
        AttachF().mirroredZ().translate([d1,-d1,0]),
        AttachF().mirroredZ().translate([d1,d1,0])
        );
}

function Core()
{
    R2 = R/2; 
    
    return union(cube(R), 
    Attach(0).rotateX(90).translate([R2,0,R2]),
    Attach(0).rotateX(-90).translate([R2,R,R2]),
    Attach(0).rotateX(90).rotateZ(-90).translate([0,R2,R2]),
    Attach(0).rotateX(-90).rotateZ(-90).translate([R,R2,R2]),
    Attach(0).translate([R2,R2,R]));
}

function Side()
{
    return difference(cube([v+R,R,sideH]), Attach(epsilon_material).translate([R/2,R/2,0]));
}

function regular_side()
{
    return difference(Side(), 
        cube([epsilon_material, 2*R,2*R]),
        cube([2*R, epsilon_material,2*R]),
        cube([2*R, epsilon_material,2*R]).translate([0,R - epsilon_material, 0])
        );
}

function xor(a, b)
{
    return union(difference(a, b), difference(b, a))
}

function attach_side()
{
    return xor(regular_side(),AttachSide(epsilon_material).translate([R/2, R/2, sideH]));
}

function plain_top()
{
    R2 = R/2
    return difference(cube([R + 2 * v, R + 2 * v, topH]),  Attach(epsilon_material).translate([R2 + v,R2 + v,0]));
}

function BottomVanil()
{
    return union(cube([R + 2 * v, R + 2 * v, v]), Core().translate([v,v,v]));
}

function bottom_attach()
{
       return difference(BottomVanil(), Attach(epsilon_material).translate([R2 + v,R2 + v,0]));
}

function top_attach()
{
    return union(plain_top(),Attach(0).translate([R2 + v,R2 + v,topH]));
}

function top0()
{
   R2= R/2;
   return union(plain_top(), Draw0(0).translate([R2+v,R2+v,topH])); 
}

function top_plus()
{
   R2= R/2;
   return union(plain_top(), DrawPlus(0).translate([R2+v,R2+v,topH])); 
}

function bottom_plus()
{
   R2= R/2;
  return difference(BottomVanil(),DrawPlus(epsilon_material).translate([R2+v,R2+v,0])); 
    
}

function bottom0()
{
   R2= R/2;
  return difference(BottomVanil(),Draw0(epsilon_material).translate([R2+v,R2+v,0])); 
    
}

function bottom_plus0()
{
    return intersection(bottom_plus(), bottom0());
}

function all()
{
  return union(regular_side().setColor([0.2,0.9,0.5]), 
  attach_side().translate([0, 3*R, 0]).setColor([0.2,0.9,0.5]),
  plain_top().translate([3*R, 9*R, 0]).setColor([1,1,0]), 
  top_attach().translate([3*R, 0, 0]).setColor([1,1,0]), 
  top0().translate([3*R, 3*R, 0]).setColor([1,1,0]),
  top_plus().translate([3*R, 6*R, 0]).setColor([1,1,0]),
  bottom_attach().translate([6 * R, 0, 0]).setColor([0.9,0.5,0.5]),
  bottom_plus().translate([6 * R, 3*R, 0]).setColor([0.9,0.5,0.5]),
  bottom0().translate([6 * R, 6*R, 0]).setColor([0.9,0.5,0.5]),
  bottom_plus0().translate([6 * R, 9*R, 0]).setColor([0.9,0.5,0.5])
  //top_plus(),
  //bottom_plus(),
  //bottom_plus0()
  );  
}

function main() {
    
    //return AttachS();
    
    //for(var i=0; i<attach_m; i+=attach_w) {
    //    v = union(v, MainAttachMale().translate([i,0,0]));
    //}
    
//     m  = attach_m;
//    h = attach_h;
//    dp = attach_dp;
//    w = attach_w;
    //difference(union(cube([m, dp, h]), MainAttachFemale(), MainAttachFemale().mirroredX().translate([m, 0, 0])),cube([m, dp, h]).rotateX(-45)); 
    //return difference(union(cube([m, dp, h]), MainAttachFemale()),cube([m, dp, 2*h]).rotateX(-45));
    
   //return union(v, AttachEmale());
   //return AttachEfemale();
   return all().translate([-5*R, -5*R, 0]);
}
