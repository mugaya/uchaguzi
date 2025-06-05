from django.shortcuts import render
from .models import Presidential34B, PresidentialResult


def maps(request, mid=1):
    """Page to render home."""
    try:
        datas, pbs = {}, [11, 55, 182, 271]
        tally = 0
        if mid > 1:
            return mapdata(request, mid)
        results = Presidential34B.objects.filter(year=2022)
        for result in results:
            cid = result.constituency_id
            asp = 0 if result.asp1 == 0 else 1
            if cid in pbs:
                asp = 3
            if asp == 1:
                tally += 1
                asp = 2 if result.asp2 > result.asp1 else 1
            datas[cid] = asp
        context = {}
        context['datas'] = datas
        context['tally'] = '%s/291' % tally
        context['page_header'] = 'Contact us'
        return render(request, 'maps.html', context)
    except Exception as e:
        raise e
    else:
        pass


def mapdata(request, mid):
    """Page to render home."""
    try:
        datas = {}
        results = PresidentialResult.objects.filter(year=2022)
        for result in results:
            cid = result.county_id
            vt = ((result.valid_votes + result.rej_votes) / result.reg_voters) * 100
            datas[cid] = vt
            print(cid, vt)
        context = {}
        context['datas'] = datas
        context['page_header'] = '2022 Election Turn out'
        return render(request, 'county_maps.html', context)
    except Exception as e:
        raise e
    else:
        pass
