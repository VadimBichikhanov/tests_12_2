from collections import OrderedDict
import unittest
from runner import Runner
from tournament import Tournament


class TournamentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.all_results = OrderedDict()
        cls.test_descriptions = {
            1: "Усэйн и Ник",
            2: "Андрей и Ник",
            3: "Усэйн, Андрей и Ник",
            4: "Различные дистанции: 50",
            5: "Различные дистанции: 100",
            6: "Различные дистанции: 150",
            7: "Отсутствие участников",
            8: "Один участник",
            9: "Один участник",
            10: "Один участник"
        }

    def setUp(self):
        self.usain = Runner(name="Усэйн", speed=10)
        self.andrey = Runner(name="Андрей", speed=9)
        self.nik = Runner(name="Ник", speed=3)

    @classmethod
    def tearDownClass(cls):
        def assert_with_error_handling(test_func, error_message, test_instance, *args):
            try:
                test_func(test_instance, *args)
            except AssertionError as e:
                print(f"Ошибка в тесте {key}: {error_message}. Подробности: {e}")

        def check_slowest_participant_last(ti, v, lp, sp):
            ti.assertTrue(v[lp] == sp, f"Участник с наименьшей скоростью ({sp.name}) не на последнем месте")

        def check_expected_participants(ti, v, ep):
            ti.assertEqual(len(v), ep, f"Количество участников не соответствует ожидаемому: ожидалось {ep}, получено {len(v)}")

        def check_all_participants_finished(ti, v, ap):
            ti.assertTrue(all(runner.name in ap for runner in v.values()), "Не все участники финишировали")

        def check_results_match_expectations(ti, v):
            ti.assertTrue(all(v[time] == cls.all_results[key][time] for time in v), "Результаты не соответствуют ожиданиям")

        def check_fastest_participant_first(ti, v, fp, fsp):
            ti.assertEqual(v[fp], fsp, f"Участник с наибольшей скоростью ({fsp.name}) не финишировал первым")

        def check_slowest_participant_not_first(ti, v, fp, sp):
            ti.assertNotEqual(v[fp], sp, f"Участник с наименьшей скоростью ({sp.name}) финишировал первым")

        def check_fastest_time_less_than_slowest_time(ti, lp, fp):
            ti.assertGreater(lp, fp, f"Время финиширования участника с наибольшей скоростью ({fp:.2f}) не меньше времени финиширования участника с наименьшей скоростью ({lp:.2f})")

        for key, value in cls.all_results.items():
            description = cls.test_descriptions.get(key, "Описание отсутствует")
            result_str = {place: f"{runner.name}" for place, (time, runner) in enumerate(sorted(value.items()), start=1)}
            print(f"Тест {key}: {description}")
            print(result_str)
            if value:
                slowest_participant = min(value.values(), key=lambda runner: runner.speed)
                last_place = max(value.keys())
                test_instance = cls()
                expected_participants = len(cls.all_results[key])
                all_participants = set(runner.name for runner in cls.all_results[key].values())

                assert_with_error_handling(
                    check_slowest_participant_last,
                    f"Участник с наименьшей скоростью ({slowest_participant.name}) не на последнем месте",
                    test_instance,
                    value,
                    last_place,
                    slowest_participant
                )
                assert_with_error_handling(
                    check_expected_participants,
                    f"Количество участников не соответствует ожидаемому: ожидалось {expected_participants}, получено {len(value)}",
                    test_instance,
                    value,
                    expected_participants
                )
                assert_with_error_handling(
                    check_all_participants_finished,
                    "Не все участники финишировали",
                    test_instance,
                    value,
                    all_participants
                )
                assert_with_error_handling(
                    check_results_match_expectations,
                    "Результаты не соответствуют ожиданиям",
                    test_instance,
                    value
                )
                fastest_participant = max(value.values(), key=lambda runner: runner.speed)
                first_place = min(value.keys())
                assert_with_error_handling(
                    check_fastest_participant_first,
                    f"Участник с наибольшей скоростью ({fastest_participant.name}) не финишировал первым",
                    test_instance,
                    value,
                    first_place,
                    fastest_participant
                )
                assert_with_error_handling(
                    check_slowest_participant_not_first,
                    f"Участник с наименьшей скоростью ({slowest_participant.name}) финишировал первым",
                    test_instance,
                    value,
                    first_place,
                    slowest_participant
                )
                assert_with_error_handling(
                    check_fastest_time_less_than_slowest_time,
                    f"Время финиширования участника с наибольшей скоростью ({first_place:.2f}) не меньше времени финиширования участника с наименьшей скоростью ({last_place:.2f})",
                    test_instance,
                    last_place,
                    first_place
                )

    def run_race_test(self, participants, test_number, distance=90):
        tournament = Tournament(distance, *participants)
        result = tournament.start()
        self.all_results[test_number] = result

    def test_races(self):
        race_configurations = [
            ([self.usain, self.nik], 1),
            ([self.andrey, self.nik], 2),
            ([self.usain, self.andrey, self.nik], 3)
        ]
        for participants, test_number in race_configurations:
            self.run_race_test(participants, test_number)

    def test_different_distances(self):
        distances = [50, 100, 150]
        for i, distance in enumerate(distances, start=4):
            self.run_race_test([self.usain, self.andrey, self.nik], i, distance)

    def test_no_participants(self):
        self.run_race_test([], 7)

    def test_single_participant(self):
        participants = [self.usain, self.andrey, self.nik]
        for i, participant in enumerate(participants, start=8):
            self.run_race_test([participant], i)



if __name__ == '__main__':
    unittest.main()