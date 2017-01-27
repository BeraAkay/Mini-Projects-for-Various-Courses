tr1=randi([0 1],1,4500);
tr2=randi([0 1],1,2500);
tr3=randi([0 1],1,2000);
tr4=randi([0 1],1,1200);%generated bits

users=containers.Map;
users('user1')=tr1;
users('user2')=tr2;
users('user3')=tr3;
users('user4')=tr4;%put bits for each user into map

userlen=[];

for user=keys(users);
    userbits=users(cell2mat(user));
    userlen=[userlen; [ strcat(num2str(length(userbits)),'_',user)]];%listed all users with their bit lengths
end

userlen=sort(userlen);%sorted users by bit lengths
usertime=[];
c=0;
alloc=[400,300,200,100];

for user=keys(users);%paired users with allocation
    usertime=[usertime cellstr((strcat(num2str(alloc(c+1)),'_',cell2mat(userlen(length(userlen)-c)))))];
    c=c+1;
end

userna=containers.Map(keys(users),zeros(1,4));
userut=containers.Map;
userut('user1')=[];
userut('user2')=[];
userut('user3')=[];
userut('user4')=[];
user_alloc=containers.Map;
%Q2
for unit=[1,2,3,4,5,6,7,8,9,10];%10 unit time = 2 frames
    for user=usertime;
        userd=strsplit(cell2mat(user),'_');%splitting the info (allocation_bitamount_username)
        usern=userd(3);
        if userna(cell2mat((usern)))==1;%if user finishes bits , then that user is passed in the next unit time
        else
            datan=userd(2);
            allo=userd(1);
            user_alloc(cell2mat(usern))=allo;
            data=users(cell2mat(usern));
            if length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))))>=str2num(cell2mat(allo));%checking if the user will fully use allocated time
                leftdata=[length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan)))) usern];
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) 1];%100% usage if user uses channel fully
            else;
                leftdata=length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))));%if not the left data is sent
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) leftdata/str2num(cell2mat(allo))];%the percentage of utilization is calculated
                userna(cell2mat(usern))=1;
            end
        end
    end
end
net_userut=containers.Map;
disp('2 Frames')
for us=keys(userut);
    disp(us)
    net_userut(cell2mat(us))=sum(userut(cell2mat(us)))/length(userut(cell2mat(us)));%taking the mean for utilization per unit time to find total utilization
    disp(net_userut(cell2mat(us)))
end
disp('Press Any Key to Continue')
pause()
%Q3 
%same as the previous part , just 1 frame more
for unit=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
    for user=usertime;
        userd=strsplit(cell2mat(user),'_');
        usern=userd(3);
        if userna(cell2mat((usern)))==1;
        else
            datan=userd(2);
            allo=userd(1);
            user_alloc(cell2mat(usern))=allo;
            data=users(cell2mat(usern));
            if length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))))>=str2num(cell2mat(allo));
                leftdata=[length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan)))) usern];
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) 1];
            else;
                leftdata=length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))));
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) leftdata/str2num(cell2mat(allo))];
                userna(cell2mat(usern))=1;
            end
        end
    end
end
net_userut=containers.Map;
disp('3 Frames')
for us=keys(userut);
    disp(us)
    net_userut(cell2mat(us))=sum(userut(cell2mat(us)))/length(userut(cell2mat(us)));
    disp(net_userut(cell2mat(us)))
end
disp('Press Any Key to Continue')
pause()
%Q4
%same algorithm as the previous parts , just 2 more users
tr1=randi([0 1],1,4500);
tr2=randi([0 1],1,2500);
tr3=randi([0 1],1,2000);
tr4=randi([0 1],1,1200);
tr5=randi([0 1],1,5000);
tr6=randi([0 1],1,1000);

users=containers.Map;
users('user1')=tr1;
users('user2')=tr2;
users('user3')=tr3;
users('user4')=tr4;
users('user5')=tr5;
users('user6')=tr6;


userlen=[];

for user=keys(users);
    userbits=users(cell2mat(user));
    userlen=[userlen; [ strcat(num2str(length(userbits)),'_',user)]];
end

userlen=sort(userlen);
usertime=[];
c=0;
alloc=[300,250,200,150,50,50];

for user=keys(users);
    usertime=[usertime cellstr((strcat(num2str(alloc(c+1)),'_',cell2mat(userlen(length(userlen)-c)))))];
    c=c+1;
end

userna=containers.Map(keys(users),zeros(1,6));
userut=containers.Map;
userut('user1')=[];
userut('user2')=[];
userut('user3')=[];
userut('user4')=[];
userut('user5')=[];
userut('user6')=[];
user_alloc=containers.Map;
for unit=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15];
    for user=usertime;
        userd=strsplit(cell2mat(user),'_');
        usern=userd(3);
        if userna(cell2mat((usern)))==1;
        else
            datan=userd(2);
            allo=userd(1);
            user_alloc(cell2mat(usern))=allo;
            data=users(cell2mat(usern));
            if length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))))>=str2num(cell2mat(allo));
                leftdata=[length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan)))) usern];
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) 1];
            else;
                leftdata=length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))));
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) leftdata/str2num(cell2mat(allo))];
                userna(cell2mat(usern))=1;
            end
        end
    end
end
net_userut=containers.Map;
disp('2 Extra Users with 3 Frames')
for us=keys(userut);
    disp(us)
    net_userut(cell2mat(us))=sum(userut(cell2mat(us)))/length(userut(cell2mat(us)));
    disp(net_userut(cell2mat(us)))
end


%Q5
%copy-pasted the algoritm to redo the variables and such
tr1=randi([0 1],1,4500);
tr2=randi([0 1],1,2500);
tr3=randi([0 1],1,2000);
tr4=randi([0 1],1,1200);

users=containers.Map;
users('user1')=tr1;
users('user2')=tr2;
users('user3')=tr3;
users('user4')=tr4;

userlen=[];

for user=keys(users);
    userbits=users(cell2mat(user));
    userlen=[userlen; [ strcat(num2str(length(userbits)),'_',user)]];
end

userlen=sort(userlen);
usertime=[];
c=0;
alloc=[400,300,200,100];

for user=keys(users);
    usertime=[usertime cellstr((strcat(num2str(alloc(c+1)),'_',cell2mat(userlen(length(userlen)-c)))))];
    c=c+1;
end

userna=containers.Map(keys(users),zeros(1,4));
userut=containers.Map;
userut('user1')=[];
userut('user2')=[];
userut('user3')=[];
userut('user4')=[];
user_alloc=containers.Map;
%Q2
for unit=[1:50];
    for user=usertime;
        userd=strsplit(cell2mat(user),'_');
        usern=userd(3);
        if userna(cell2mat((usern)))==1;
        else
            datan=userd(2);
            allo=userd(1);
            user_alloc(cell2mat(usern))=allo;
            data=users(cell2mat(usern));
            if length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))))>=str2num(cell2mat(allo));
                leftdata=[length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan)))) usern];
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) 1];
            else;
                leftdata=length(data(unit*str2num(cell2mat(allo))+1:str2num(cell2mat(datan))));
                userut(cell2mat((usern)))=[userut(cell2mat((usern))) leftdata/str2num(cell2mat(allo))];
                userna(cell2mat(usern))=1;
            end
        end
    end
end
disp('4 Users , 10 Frames')
for us=keys(userut);
    disp(us)
    plot([1:50],[userut(cell2mat(us)) zeros(1,50-length(userut(cell2mat(us))))])
    title(cell2mat(us))
    xlabel('Unit Time')
    ylabel('Utilization of Allocated Bits')
    legend('5*Unit Time = 1 Frame')
    disp('press Any Key for the Next Plot')
    pause()
end
disp('All the Plots Shown')