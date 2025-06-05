from django.db import connection


def get_person_ids(name, position=2, year=2022):
    """Method to search person."""
    try:
        pids = []
        tbl_name = 'county_candidates'
        print('name', name)
        if not name or len(name) == 0:
            return []
        names = name.split()

        if position == 5:
            tbl_name = 'pc_voters'
            query = ("SELECT id FROM %s WHERE to_tsvector"
                     "(ps_name)"
                     " @@ to_tsquery('english', '%s') AND year = %s")
        elif position == 2:
            query = ("SELECT id FROM %s WHERE to_tsvector"
                     "(candidate_names || ' '"
                     " || COALESCE(running_mate_names,''))"
                     " @@ to_tsquery('english', '%s') AND year = %s")
        else:
            if position == 4:
                tbl_name = 'ward_candidates'
            else:
                tbl_name = 'constituency_candidates'
            query = ("SELECT id FROM %s WHERE to_tsvector"
                     "(candidate_names)"
                     " @@ to_tsquery('english', '%s') AND year = %s")

        vals = ' & '.join(names)
        sql = query % (tbl_name, vals, year)
        print(sql)
        with connection.cursor() as cursor:
            cursor.execute(sql)
            row = cursor.fetchall()
            pids = [r[0] for r in row]
        print('res', pids)
    except Exception as e:
        print('Error with search - %s' % (str(e)))
        return []
    else:
        return pids
