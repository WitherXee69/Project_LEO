import sublist3r


def sublister(domain, threads, savefiles, verbose):
    subdomains = sublist3r.main(domain, threads, savefiles, ports=None, silent=False, verbose=verbose,
                                enable_bruteforce=False, engines=None)
    return subdomains
