from django.utils import timezone
from django.shortcuts import render
from django.db.models import Sum, Count, Q
from .settings import PIDS
from .functions import get_person_ids

from candidates.models import (
    County, Constituency, Ward, CountyCandidate,
    RegVoters, PresidentialCandidate, ConstituencyCandidate,
    WardCandidate, PCVoters, Polls, RegionCounty)

from results.models import PresidentialResult

YEAR = 2022


def home(request):
    """Page to render home."""
    try:
        context = {}
        print(request.headers)
        return render(request, 'home.html', context)
    except Exception as e:
        raise e
    else:
        pass


def position(request, pos_id, year=YEAR):
    """Page to render home."""
    try:
        pname = PIDS[pos_id] if pos_id in PIDS else ''
        page_header = '%s candidates' % (pname)
        aspirants = None
        counts = 0
        if pos_id == 'PR':
            aspirants = PresidentialCandidate.objects.filter(year=2022)
            counts = aspirants.count()
        context = {'page_header': page_header}
        context['position'] = pname
        context['aspirants'] = aspirants
        context['counts'] = counts
        return render(request, 'positions.html', context)
    except Exception as e:
        raise e
    else:
        pass


def candidate(request, pos_id, year=YEAR):
    """Page to render home."""
    try:
        return position(request, pos_id, year)

    except Exception as e:
        raise e
    else:
        pass


def parties(request, pos_id=False):
    """Page to render home."""
    try:
        counts = {'PR': 0, 'GV': 0, 'SN': 0, 'WR': 0,
                  'MP': 0, 'MC': 0, 'ALL': 0}
        governors, senators, wreps, mps, mcas = [], [], [], [], []
        candidates = CountyCandidate.objects.filter(year=2022)
        mcandidates = ConstituencyCandidate.objects.filter(year=2022)
        mca_candidates = WardCandidate.objects.filter(year=2022)
        cands = candidates.values(
            'party', 'position', 'party__name').annotate(
            dcount=Count('party')).order_by('-dcount')
        mcands = mcandidates.values(
            'party', 'party__name').annotate(
            dcount=Count('party')).order_by('-dcount')
        mcacds = mca_candidates.values(
            'party', 'party__name').annotate(
            dcount=Count('party')).order_by('-dcount')
        if pos_id:
            print('None')
            all_cds = {'GV': 2, 'SN': 3, 'WR': 4}
            acd = all_cds[pos_id] if pos_id in all_cds else 0
            if acd:
                for cds in cands:
                    if cds['position'] == acd:
                        counts[pos_id] = counts[pos_id] + cds['dcount']
                        if acd == 2:
                            governors.append(cds)
                        if acd == 3:
                            senators.append(cds)
                        if acd == 4:
                            wreps.append(cds)
            # MPs
            if pos_id == 'MP':
                for mp in mcands:
                    counts['MP'] = counts['MP'] + mp['dcount']
                    mps.append(mp)
            # MCAs
            if pos_id == 'MC':
                for mca in mcacds:
                    counts['MC'] = counts['MC'] + mca['dcount']
                    mcas.append(mca)
        else:
            counts['PR'] = 4
            for cds in cands:
                if cds['position'] == 2:
                    counts['GV'] = counts['GV'] + cds['dcount']
                    if cds['dcount'] > 10:
                        governors.append(cds)
                if cds['position'] == 3:
                    counts['SN'] = counts['SN'] + cds['dcount']
                    if cds['dcount'] > 10:
                        senators.append(cds)
                if cds['position'] == 4:
                    counts['WR'] = counts['WR'] + cds['dcount']
                    if cds['dcount'] > 10:
                        wreps.append(cds)
            # MPs
            for mp in mcands:
                counts['MP'] = counts['MP'] + mp['dcount']
                if mp['dcount'] > 10:
                    mps.append(mp)
            # MCAs
            for mca in mcacds:
                counts['MC'] = counts['MC'] + mca['dcount']
                if mca['dcount'] > 10:
                    mcas.append(mca)
        counts['ALL'] = counts['PR'] + counts['GV'] + counts['SN']
        counts['ALL'] = counts['ALL'] + counts['WR']
        counts['ALL'] = counts['ALL'] + counts['MP'] + counts['MC']
        context = {'parties': cands}
        context['governors'] = governors
        context['senators'] = senators
        context['wreps'] = wreps
        context['mps'] = mps
        context['mcas'] = mcas
        context['counts'] = counts
        context['pos_id'] = pos_id
        context['page_header'] = 'Political Parties'
        return render(request, 'parties.html', context)
    except Exception as e:
        raise e
    else:
        pass


def counties(request, county_id=False):
    """Page to render home."""
    try:
        phead = 'Counties'
        page = request.GET.get('page', 1)
        next_page = 5 if int(page) > 1 else int(page)
        stnt = (int(page) * 10) - 10
        tsnt = stnt + 10
        counties = County.objects.all()
        if not county_id:
            counties = counties.order_by('id')[stnt:tsnt]
        governors, senators, wreps = None, None, None
        cons = []
        counts = {'GV': 0, 'SN': 0, 'WR': 0, 'voters': 0}
        if county_id:
            cid = int(county_id)
            counties = counties.filter(code=county_id)
            candidates = CountyCandidate.objects.filter(county_id=county_id)
            governors = candidates.filter(position=2)
            senators = candidates.filter(position=3)
            wreps = candidates.filter(position=4)
            cons = Constituency.objects.filter(county_id=cid)
            voters = RegVoters.objects.filter(
                county_id=cid).aggregate(Sum('reg_voters'))
            counts['GV'] = governors.count()
            counts['SN'] = senators.count()
            counts['WR'] = wreps.count()
            counts['voters'] = voters['reg_voters__sum']
            phead = '%s County' % counties.first().name
        cids = counties.values_list('id')
        rvoters = RegVoters.objects.filter(
            county_id__in=cids).values('county_id').annotate(
            voters=Sum('reg_voters'))
        # Candidates
        rcands = CountyCandidate.objects.filter(
            county_id__in=cids).values('position', 'county_id').annotate(
            asps=Count('id'))
        votes, posts = {}, {}
        for voter in rvoters:
            votes[voter['county_id']] = voter['voters']
        for rcand in rcands:
            ps = {2: 0, 3: 0, 4: 0}
            if rcand['county_id'] not in posts:
                posts[rcand['county_id']] = ps
            posts[rcand['county_id']][rcand['position']] = rcand['asps']
        # More attributes
        for county in counties:
            tvote = votes[county.id] if county.id in votes else 0
            gvote = posts[county.id][2] if county.id in votes else 0
            svote = posts[county.id][3] if county.id in votes else 0
            wvote = posts[county.id][4] if county.id in votes else 0
            setattr(county, 'voters', tvote)
            setattr(county, 'GV', gvote)
            setattr(county, 'SN', svote)
            setattr(county, 'WR', wvote)
        context = {'counties': counties}
        context['governors'] = governors
        context['senators'] = senators
        context['wreps'] = wreps
        context['page_header'] = phead
        context['county_id'] = county_id
        context['cons'] = cons
        context['counts'] = counts
        context['page'] = int(page)
        context['next_page'] = next_page
        return render(request, 'counties.html', context)
    except Exception as e:
        raise e
    else:
        pass


def constituencies(request, const_id=False):
    """Page to render home."""
    try:
        phead = 'Constituencies'
        mps, consts = None, None
        counts = {'voters': 0, 'MP': 0}
        constituencies = Constituency.objects.all()
        if const_id:
            cid = int(const_id)
            constituencies = constituencies.filter(code=const_id)
            county_id = constituencies.first().county.id
            mps = ConstituencyCandidate.objects.filter(constituency_id=cid)
            cons = Ward.objects.filter(constituency_id=cid)
            consts = Constituency.objects.filter(county_id=county_id)
            voters = RegVoters.objects.filter(
                constituency_id=cid).aggregate(Sum('reg_voters'))
            counts['voters'] = voters['reg_voters__sum']
            counts['MP'] = mps.count()
            phead = '%s Constituency' % (constituencies.first().name)
        context = {'consts': constituencies}
        context['mps'] = mps
        context['cons'] = cons
        context['rels'] = constituencies
        context['counts'] = counts
        context['constituency_id'] = cid
        context['constituencies'] = consts
        mps = None
        context['page_header'] = phead
        return render(request, 'constituencies.html', context)
    except Exception as e:
        raise e
    else:
        pass


def wards(request, ward_id=False):
    """Page to render home."""
    try:
        phead = 'Wards'
        counts = {'voters': 0, 'MC': 0}
        wards = Ward.objects.all()
        if ward_id:
            cid = int(ward_id)
            mcas = WardCandidate.objects.filter(ward_id=cid)
            fwards = wards.filter(code=ward_id)
            const_id = fwards.first().constituency_id
            cons = wards.filter(constituency_id=const_id)
            wards = fwards
            voters = RegVoters.objects.filter(
                ward_id=cid).aggregate(Sum('reg_voters'))
            counts['voters'] = voters['reg_voters__sum']
            counts['MC'] = mcas.count()
            phead = '%s Ward' % (fwards.first().name)
        context = {'wards': wards}
        context['cons'] = cons
        context['rels'] = fwards
        context['mcas'] = mcas
        context['counts'] = counts
        context['ward_id'] = ward_id
        context['page_header'] = phead
        return render(request, 'wards.html', context)
    except Exception as e:
        raise e
    else:
        pass


def top(request, pos_id):
    """Page to render home."""
    try:
        all_cds = {'GV': 2, 'SN': 3, 'WR': 4}
        counts = 0
        pname = ''
        candidates, mps, mcas = None, None, None
        if pos_id:
            if pos_id in all_cds:
                pname = PIDS[pos_id] if pos_id in PIDS else ''
                position = all_cds[pos_id]
                candidates = CountyCandidate.objects.filter(
                    year=2022, position=position)
                counts = candidates.count()
                candidates = candidates.values(
                    'county_id', 'county__name').annotate(
                    dcount=Count('id')).order_by('-dcount')
            if pos_id == 'MP':
                pname = 'Member of National Assembly'
                mps = ConstituencyCandidate.objects.filter(
                    year=2022)
                counts = mps.count()
                mps = mps.values(
                    'constituency_id', 'constituency__name',
                    'county__name').annotate(
                    dcount=Count('id')).order_by('-dcount')
            if pos_id == 'MC':
                pname = 'Member of County Assembly'
                mcas = WardCandidate.objects.filter(
                    year=2022)
                counts = mcas.count()
                mcas = mcas.values(
                    'ward_id', 'ward__name', 'constituency__name',
                    'county__name').annotate(
                    dcount=Count('id')).order_by('-dcount')
        context = {}
        context['candidates'] = candidates
        context['mps'] = mps
        context['mcas'] = mcas
        context['counts'] = counts
        context['pname'] = pname
        context['page_header'] = 'Top Contestants'
        return render(request, 'top.html', context)
    except Exception as e:
        raise e
    else:
        pass


def search(request):
    """Page to render home."""
    try:
        context = {}
        name = request.GET.get('s', '')
        category = request.GET.get('category', 2)
        cat_id = int(category)
        pids = get_person_ids(name, cat_id, YEAR)
        results, mresults, wresults, presults = [], [], [], []
        if pids:
            if cat_id == 5:
                presults = PCVoters.objects.filter(id__in=pids, year=YEAR)
            elif cat_id == 4:
                if pids:
                    wresults = WardCandidate.objects.filter(id__in=pids)
                else:
                    wresults = WardCandidate.objects.filter(
                        Q(
                            ward__name__icontains=name) | Q(
                            party__name__icontains=name) | Q(
                            party__abbrev__icontains=name))
                wresults = wresults.filter(year=YEAR)
            elif cat_id == 3:
                if pids:
                    mresults = ConstituencyCandidate.objects.filter(
                        id__in=pids)
                else:
                    mresults = ConstituencyCandidate.objects.filter(
                        Q(
                            constituency__name__icontains=name) | Q(
                            party__name__icontains=name) | Q(
                            party__abbrev__icontains=name))
                mresults = mresults.filter(year=YEAR)
            else:
                if pids:
                    results = CountyCandidate.objects.filter(id__in=pids)
                else:
                    results = CountyCandidate.objects.filter(
                        Q(
                            county__name__icontains=name) | Q(
                            party__name__icontains=name) | Q(
                            party__abbrev__icontains=name))
                results = results.filter(year=YEAR)
        context['page_header'] = 'Search'
        context['results'] = results
        context['mresults'] = mresults
        context['wresults'] = wresults
        context['presults'] = presults
        context['name'] = name
        context['category'] = cat_id
        return render(request, 'search.html', context)
    except Exception as e:
        raise e
    else:
        pass


def ps(request, rid=0, area_id=None):
    """Page to render home."""
    try:
        p_centers, c_centers = [], []
        w_centers, r_centers = [], []
        areas, area_name = [], 'Kenya'
        counts = {'total_voters': 0, 'total_ps': 0}
        if int(rid) == 2:
            aid = int(area_id) if area_id else 1
            c_centers = PCVoters.objects.filter(county_id=aid).values(
                'constituency__code', 'constituency__name').annotate(
                t_voters=Sum('reg_voters'),
                t_ps=Sum('ps_stations')).order_by('-t_voters')
            pss = c_centers
            area = County.objects.get(id=aid)
            area_name = '%s County' % (area.name)
            areas = County.objects.filter(id__gte=aid)[:10]
        elif int(rid) == 3:
            aid = int(area_id) if area_id else 1
            w_centers = PCVoters.objects.filter(constituency_id=aid).values(
                'ward__code', 'ward__name').annotate(
                t_voters=Sum('reg_voters'),
                t_ps=Sum('ps_stations')).order_by('-t_voters')
            pss = w_centers
            area = Constituency.objects.get(id=aid)
            cid = area.county_id
            area_name = '%s Constituency' % (area.name)
            areas = Constituency.objects.filter(county_id=cid)
        elif int(rid) == 4:
            aid = int(area_id) if area_id else 1
            r_centers = PCVoters.objects.filter(ward_id=aid).values(
                'ps_code', 'ps_name').annotate(
                t_voters=Sum('reg_voters'),
                t_ps=Sum('ps_stations')).order_by('-t_voters')
            pss = r_centers
            area = Ward.objects.get(id=aid)
            cid = area.constituency_id
            area_name = '%s Ward' % (area.name)
            areas = Ward.objects.filter(constituency_id=cid)
        else:
            p_centers = PCVoters.objects.values(
                'county__code', 'county__name').annotate(
                t_voters=Sum('reg_voters'),
                t_ps=Sum('ps_stations')).order_by('-t_voters')
            pss = p_centers
        for ps in pss:
            counts['total_voters'] = counts['total_voters'] + ps['t_voters']
            counts['total_ps'] = counts['total_ps'] + ps['t_ps']
        context = {}
        context['p_centers'] = p_centers
        context['c_centers'] = c_centers
        context['w_centers'] = w_centers
        context['r_centers'] = r_centers
        context['counts'] = counts
        context['area_name'] = area_name
        context['areas'] = areas
        context['rid'] = int(rid)
        return render(request, 'polling_centers.html', context)
    except Exception as e:
        raise e
    else:
        pass


def pc(request, rid, ward_id):
    """Page to render home."""
    try:
        return ps(request, rid, ward_id)
    except Exception as e:
        raise e
    else:
        pass


def polls(request):
    """Page to render home."""
    try:
        pname = 'Presidential'
        votes = {'total_voters': 0, 'total_asp1': 0, 'total_asp2': 0,
                 'total_asp3': 0, 'total_asp4': 0, 'total_casp1': 0,
                 'total_casp2': 0, 'total_casp3': 0, 'total_casp4': 0}
        aspirants = PresidentialCandidate.objects.filter(year=2022)
        voters = PCVoters.objects.values(
            'county_id', 'county__code', 'county__name').annotate(
            t_voters=Sum('reg_voters')).order_by('-t_voters')
        counts = aspirants.count()
        today = timezone.now()
        # Get the polls
        regions = RegionCounty.objects.all()
        polls = Polls.objects.filter(poll_id=1)
        rpolls, cpolls = {}, {}
        for poll in polls:
            all_asps = {'asp1': 0, 'asp2': 0, 'asp3': 0, 'asp4': 0}
            if poll.region_id not in rpolls:
                rpolls[poll.region_id] = all_asps
                rpolls[poll.region_id]['asp1'] = poll.asp1
                rpolls[poll.region_id]['asp2'] = poll.asp2
                rpolls[poll.region_id]['asp3'] = poll.asp3
                rpolls[poll.region_id]['asp4'] = poll.asp4
        for region in regions:
            rid = region.region_id
            cid = region.county_id
            rpoll = rpolls[rid] if rid in rpolls else {}
            cpolls[cid] = rpoll
        # print(cpolls)
        # print(voters)
        for ps in voters:
            t_votes = ps['t_voters']
            cid = ps['county_id']
            asp1 = t_votes * (cpolls[cid]['asp1'] / 100) * 0.7741
            asp2 = t_votes * (cpolls[cid]['asp2'] / 100) * 0.7741
            asp3 = t_votes * (cpolls[cid]['asp3'] / 100) * 0.7741
            asp4 = t_votes * (cpolls[cid]['asp4'] / 100) * 0.7741
            ps['asp1'] = int(asp1)
            ps['asp2'] = int(asp2)
            ps['asp3'] = int(asp3)
            ps['asp4'] = int(asp4)
            ps['pasp1'] = int((asp1 / t_votes) * 100)
            ps['pasp2'] = int((asp2 / t_votes) * 100)
            ps['pasp3'] = int((asp3 / t_votes) * 100)
            ps['pasp4'] = int((asp4 / t_votes) * 100)
            votes['total_voters'] = votes['total_voters'] + ps['t_voters']
            votes['total_asp1'] = votes['total_asp1'] + ps['asp1']
            votes['total_asp2'] = votes['total_asp2'] + ps['asp2']
            votes['total_asp3'] = votes['total_asp3'] + ps['asp3']
            votes['total_asp4'] = votes['total_asp4'] + ps['asp4']
            # Count for > 25
            if (asp1 / t_votes) >= 0.25:
                votes['total_casp1'] = votes['total_casp1'] + 1
            if (asp2 / t_votes) >= 0.25:
                votes['total_casp2'] = votes['total_casp2'] + 1
            if (asp3 / t_votes) >= 0.25:
                votes['total_casp3'] = votes['total_casp3'] + 1
            if (asp4 / t_votes) >= 0.25:
                votes['total_casp4'] = votes['total_casp4'] + 1
        # Add totals
        cast_votes = votes['total_voters'] * 0.7741
        votes['total_pasp1'] = int((votes['total_asp1'] / cast_votes) * 100)
        votes['total_pasp2'] = int((votes['total_asp2'] / cast_votes) * 100)
        votes['total_pasp3'] = int((votes['total_asp3'] / cast_votes) * 100)
        votes['total_pasp4'] = int((votes['total_asp4'] / cast_votes) * 100)
        context = {'page_header': '%s Opinion Polls' % (pname)}
        context['pname'] = pname
        context['aspirants'] = aspirants
        context['counts'] = counts
        context['counties'] = voters
        context['today'] = today
        context['votes'] = votes
        return render(request, 'polls.html', context)
    except Exception as e:
        raise e
    else:
        pass


def result(request, pos_id, year=2022):
    """Page to render home."""
    try:
        aspirants = None
        counts = 0
        pname = ''
        votes = {'total_voters': 0, 'total_rejected': 0, 'total_valid': 0}
        if pos_id == 'PR':
            pname = 'Presidential'
            aspirants = PresidentialCandidate.objects.filter(
                year=year).order_by('cid')
            for asp in aspirants:
                votes['asp%s' % asp.cid] = 0
                votes['total_asp%s' % asp.cid] = 0
                votes['total_casp%s' % asp.cid] = 0
                votes['asp%s_name' % asp.cid] = asp.candidate_names.split()[0]
            counts = aspirants.count()
            voters = PresidentialResult.objects.filter(year=year).values(
                'county_id', 'county__code', 'county__name', 'asp1',
                'asp2', 'asp3', 'asp4', 'asp5', 'asp6', 'asp7', 'asp8',
                'valid_votes', 'rej_votes').annotate(
                t_voters=Sum('reg_voters')).order_by('-t_voters')
        for ps in voters:
            votes['total_voters'] = votes['total_voters'] + ps['t_voters']
            votes['total_rejected'] = votes['total_rejected'] + ps['rej_votes']
            votes['total_valid'] = votes['total_valid'] + ps['valid_votes']
            cast_votes = ps['valid_votes'] + ps['rej_votes']
            for asp in aspirants:
                tid = 'asp%s' % asp.cid
                ps[tid] = ps[tid]
                tperc = 0
                if cast_votes > 0:
                    tperc = round((ps[tid] / cast_votes) * 100, 2)
                ps['p%s' % tid] = tperc
                if ps['p%s' % tid] > 25:
                    votes['total_c%s' % tid] = votes['total_c%s' % tid] + 1
                votes['total_%s' % tid] = votes['total_%s' % tid] + ps[tid]
            ps['turnout'] = round((cast_votes / ps['t_voters'] * 100), 1)
        for asp in aspirants:
            tid = 'asp%s' % asp.cid
            total_cast = votes['total_valid'] + votes['total_rejected']
            county_perc = 0
            if total_cast > 0:
                county_perc = (votes['total_%s' % tid] / total_cast) * 100
            votes['total_p%s' % tid] = round(county_perc, 2)
        total_cast = votes['total_rejected'] + votes['total_valid']
        avg_turnout = 0
        if votes['total_voters'] > 0:
            avg_turnout = round((total_cast / votes['total_voters']) * 100, 2)
        votes['turnout'] = avg_turnout
        today = timezone.now()
        context = {'page_header': '%s %s Results' % (year, pname)}
        context['pname'] = pname
        context['aspirants'] = aspirants
        context['counts'] = counts
        context['counties'] = voters
        context['today'] = today
        context['votes'] = votes
        context['year'] = year
        return render(request, 'results.html', context)
    except Exception as e:
        raise e
    else:
        pass


def results(request, pos_id, year):
    """Page to render home."""
    try:
        return result(request, pos_id, year)
    except Exception as e:
        raise e
    else:
        pass


def vote(request):
    """Page to render home."""
    try:
        context = {}
        context['page_header'] = 'Where and who to Vote'
        return render(request, 'vote.html', context)
    except Exception as e:
        raise e
    else:
        pass


def contact(request):
    """Page to render home."""
    try:
        context = {}
        context['page_header'] = 'Contact us'
        return render(request, 'contact.html', context)
    except Exception as e:
        raise e
    else:
        pass
