function input=cv_graph(family,D,seed)
% CV independently reproducible synthetic graph; no optimizer RNG calls.
assert(any(strcmp(family,{'er','block','hub'}))&&any(D==[80,160]));
assert(seed>=0&&seed<2^32&&seed==fix(seed));state=double(seed);A=false(D);
for i=1:D-1
 for j=i+1:D
  if strcmp(family,'er'),p=4/D;
  elseif strcmp(family,'block'),if ceil(i/10)==ceil(j/10),p=.32;else,p=1/D;end
  else,if i<=4||j<=4,p=.32;else,p=1.6/D;end
  end
  if draw()<p,A(i,j)=true;A(j,i)=true;end
 end
end
for i=1:D,j=1+mod(i,D);A(i,j)=true;A(j,i)=true;end
order=1:D;
for i=D:-1:2,j=1+floor(draw()*i);tmp=order(i);order(i)=order(j);order(j)=tmp;end
w=zeros(D,1);w(order(1:round(.7*D)))=1;C=double(A|logical(eye(D)));
input=struct('schema','CV_INPUT_V1','family',family,'D',D,'graph_seed',seed,'C',C,'w',w, ...
 'generator','LCG32_1664525_1013904223','final_graph_state',state,'biological_data',false);
 function u=draw()
  state=mod(1664525*state+1013904223,4294967296);u=state/4294967296;
 end
end
