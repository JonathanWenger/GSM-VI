import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["XLA_PYTHON_CLIENT_PREALLOCATE"]="false"
os.environ["XLA_PYTHON_CLIENT_ALLOCATOR"]="platform"

# enable 16 bit precision for jax
from jax import config
config.update("jax_enable_x64", True)

import jax
import jax.numpy as jnp
from jax import jit, grad, random
import optax

import numpyro
import numpyro.distributions as dist

# Import GSM
import sys
sys.path.append('../src/')
from advi import ADVI

#####


#####
#####
def setup_model(D=10):
   
    # setup a Gaussian target distribution
    mean = np.random.random(D)
    L = np.random.normal(size = D**2).reshape(D, D)
    cov = np.matmul(L, L.T) + np.eye(D)*1e-3
    model = dist.MultivariateNormal(loc=mean, covariance_matrix=cov)
    lp = jit(lambda x: jnp.sum(model.log_prob(x)))
    lp_g = jit(grad(lp, argnums=0))

    return mean, cov, lp, lp_g


def advi_fit(D, lp, lp_g, lr=1e-2, batch_size=16, niter=1000):

    advi = ADVI(D=D, lp=lp)
    key = random.PRNGKey(99)
    opt = optax.adam(learning_rate=lr)
    mean_fit, cov_fit, losses = advi.fit(key, opt, batch_size=batch_size, niter=niter)

    return mean_fit, cov_fit



if __name__=="__main__":
    
    D = 5
    mean, cov, lp, lp_g = setup_model(D=D)

    niter = 5000
    lr = 5e-3
    batch_size = 16
    mean_fit, cov_fit = advi_fit(D, lp, lp_g, lr=lr, batch_size=batch_size, niter=niter)

    print("True mean : ", mean)
    print("Fit mean  : ", mean_fit)
    print()
    print("True covariance matrix : \n", cov)
    print("Fit covariance matrix  : \n", cov_fit)
