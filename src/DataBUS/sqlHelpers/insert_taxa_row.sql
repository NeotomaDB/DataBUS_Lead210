SELECT ts.inserttaxon(_code := 'Cumulative Dry Mass',
                      _name := 'Cumulative Dry Mass',
                      _extinct := False,
                      _groupid := 'LAB');

-- '210Pb/210Po' ?? Alpha vs Supported
SELECT ts.inserttaxon(_code := '210Pb/210Po',
                      _name := '210Pb/210Po',
                      _extinct := False,
                      _groupid := 'LAB');

-- 210pb
SELECT ts.inserttaxon(_code := '210Pb',
                      _name := 'Pb210',
                      _extinct := False,
                      _groupid := 'LAB');


-- '137Cs'
SELECT ts.inserttaxon(_code := '137Cs',
                      _name := '137Cs',
                      _extinct := False,
                      _groupid := 'LAB');


-- '214Bi'
SELECT ts.inserttaxon(_code := '214Bi',
                      _name := '214Bi',
                      _extinct := False,
                      _groupid := 'LAB');


-- '214Pb'
SELECT ts.inserttaxon(_code := '214Pb',
                      _name := '214Pb',
                      _extinct := False,
                      _groupid := 'LAB');

-- 'dry mass accumulation rate'
SELECT ts.inserttaxon(_code := 'dry mass accumulation rate',
                      _name := 'dry mass accumulation rate',
                      _extinct := False,
                      _groupid := 'LAB');
--'210pb'
SELECT ts.inserttaxon(_code := '210pb',
                      _name := '210pb',
                      _extinct := False,
                      _groupid := 'LAB');

--'excess 210pb'
SELECT ts.inserttaxon(_code := 'excess 210pb',
                      _name := 'excess 210pb',
                      _extinct := False,
                      _groupid := 'LAB');