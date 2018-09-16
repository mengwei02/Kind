function [idx,idc,itr,err,H,V]=outlier_tolerant(Uk,mu,prt)
%====================================================================
% Solving K-indicators by Alternating Projection algorithm with 
% Outlier-tolerant. (KindAP)
%
% Copyright: Yuchen Yang, Yin Zhang. 2018
%
%====================================================================
% Input:
% Uk: n by k column-orthonormal matrix
%     (usually k eigenvectors of a Gram or Laplacian matrix)
% mu: the parameter of strength of outliers
% prt: whether printing the residual curve or not
%====================================================================
% Output:
% idc: indices detected as outliers
% idx: cluster indices for data points
%   H: n by k indicator matrix
% itr: number of iterations
% err: the objective function value of outlier-tolerant K-indicators
%====================================================================

    max_itr = 10;  
    err = [];
    idc_old = [];
    U = Uk;
    for itr=1:max_itr
        [~,index,~,H,Z]=kind_ap(U,0,0);
        T=H*Z'-Uk;
        V=prox_l2(T,mu);
        err = [err;0.5*norm(V-T,'fro')^2+mu*sum(vecnorm(V,2,2))];
        idc = find(max(abs(V),[],2)~=0);
        idx = index(max(abs(V),[],2)==0);
        crit1 = itr==1 || abs(err(end)-err(end-1))/err(end-1)>1e-5;
        crit2 = length(idc)~=length(idc_old) || ~norm(idc-idc_old,1);
        if ~crit1||~crit2
            break;
        end
        idc_old = idc;
        [Q,R] = qr(V+Uk,0);
        [Sr,~,Dr]=svd(R);
        U = Q*(Sr*Dr');
% plan B
% solve orthogonality constraints by admm/augmented Lag;
    end
    
    if prt
        figure;
        plot(err,'-r');
        title('The iterative value of 1/2||V-HZ^T||_F^2+\mu||V-U_k||_{2,1}');
    end
end

% Solve soft thresholding with l2 norm
function X=prox_l2(T,mu)
    X = zeros(size(T));
    for i=1:size(T,1)
        t=T(i,:);
        nrm=norm(t,2);
        if nrm<mu
            x=zeros(size(t));
        else
            x=(1-mu/nrm)*t;
        end
        X(i,:)=x;
    end
end
    
    