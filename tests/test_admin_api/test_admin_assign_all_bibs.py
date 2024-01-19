from http import HTTPStatus

from freezegun import freeze_time

import shared.api.api_errors as ae

from tests.conftest import BaseTest, before_cutoff, after_cutoff


origin = "api_admin_assign_all_bibs"

correct_admin_assign_all_response = {
    "assignedBibs": [
        {"bib_no": 1, "licence_no": "1144414"},
        {"bib_no": 2, "licence_no": "1176575"},
        {"bib_no": 3, "licence_no": "1360829"},
        {"bib_no": 4, "licence_no": "1407687"},
        {"bib_no": 5, "licence_no": "1472537"},
        {"bib_no": 6, "licence_no": "1542192"},
        {"bib_no": 7, "licence_no": "1728286"},
        {"bib_no": 8, "licence_no": "1804632"},
        {"bib_no": 9, "licence_no": "1865934"},
        {"bib_no": 10, "licence_no": "2025398"},
        {"bib_no": 11, "licence_no": "2148803"},
        {"bib_no": 12, "licence_no": "2184884"},
        {"bib_no": 13, "licence_no": "2414528"},
        {"bib_no": 14, "licence_no": "2423118"},
        {"bib_no": 15, "licence_no": "2721321"},
        {"bib_no": 16, "licence_no": "3029833"},
        {"bib_no": 17, "licence_no": "3107950"},
        {"bib_no": 18, "licence_no": "3115440"},
        {"bib_no": 19, "licence_no": "3131351"},
        {"bib_no": 20, "licence_no": "3172916"},
        {"bib_no": 21, "licence_no": "3611348"},
        {"bib_no": 22, "licence_no": "3680058"},
        {"bib_no": 23, "licence_no": "3756914"},
        {"bib_no": 24, "licence_no": "3821971"},
        {"bib_no": 25, "licence_no": "3869449"},
        {"bib_no": 26, "licence_no": "3937734"},
        {"bib_no": 27, "licence_no": "3959984"},
        {"bib_no": 28, "licence_no": "4024540"},
        {"bib_no": 29, "licence_no": "4092267"},
        {"bib_no": 30, "licence_no": "4408434"},
        {"bib_no": 31, "licence_no": "4481832"},
        {"bib_no": 32, "licence_no": "4513266"},
        {"bib_no": 33, "licence_no": "4527982"},
        {"bib_no": 34, "licence_no": "4529052"},
        {"bib_no": 35, "licence_no": "4529894"},
        {"bib_no": 36, "licence_no": "4530477"},
        {"bib_no": 37, "licence_no": "4530487"},
        {"bib_no": 38, "licence_no": "4530898"},
        {"bib_no": 39, "licence_no": "4531022"},
        {"bib_no": 40, "licence_no": "4568441"},
        {"bib_no": 41, "licence_no": "4586873"},
        {"bib_no": 42, "licence_no": "4706306"},
        {"bib_no": 43, "licence_no": "4769385"},
        {"bib_no": 44, "licence_no": "4789239"},
        {"bib_no": 45, "licence_no": "4797847"},
        {"bib_no": 46, "licence_no": "4881098"},
        {"bib_no": 47, "licence_no": "4957999"},
        {"bib_no": 48, "licence_no": "5135408"},
        {"bib_no": 49, "licence_no": "5261644"},
        {"bib_no": 50, "licence_no": "5326610"},
        {"bib_no": 51, "licence_no": "5327529"},
        {"bib_no": 52, "licence_no": "5328103"},
        {"bib_no": 53, "licence_no": "5328211"},
        {"bib_no": 54, "licence_no": "5332041"},
        {"bib_no": 55, "licence_no": "5421435"},
        {"bib_no": 56, "licence_no": "5429203"},
        {"bib_no": 57, "licence_no": "5437003"},
        {"bib_no": 58, "licence_no": "5442008"},
        {"bib_no": 59, "licence_no": "5664867"},
        {"bib_no": 60, "licence_no": "5756925"},
        {"bib_no": 61, "licence_no": "5853287"},
        {"bib_no": 62, "licence_no": "6056636"},
        {"bib_no": 63, "licence_no": "6112979"},
        {"bib_no": 64, "licence_no": "6200681"},
        {"bib_no": 65, "licence_no": "6346867"},
        {"bib_no": 66, "licence_no": "6387841"},
        {"bib_no": 67, "licence_no": "6445854"},
        {"bib_no": 68, "licence_no": "6474645"},
        {"bib_no": 69, "licence_no": "6493933"},
        {"bib_no": 70, "licence_no": "6577883"},
        {"bib_no": 71, "licence_no": "6674184"},
        {"bib_no": 72, "licence_no": "6721087"},
        {"bib_no": 73, "licence_no": "6762347"},
        {"bib_no": 74, "licence_no": "7037025"},
        {"bib_no": 75, "licence_no": "7059004"},
        {"bib_no": 76, "licence_no": "7078876"},
        {"bib_no": 77, "licence_no": "7207784"},
        {"bib_no": 78, "licence_no": "7214813"},
        {"bib_no": 79, "licence_no": "7216286"},
        {"bib_no": 80, "licence_no": "7216475"},
        {"bib_no": 81, "licence_no": "7218408"},
        {"bib_no": 82, "licence_no": "7218763"},
        {"bib_no": 83, "licence_no": "7219314"},
        {"bib_no": 84, "licence_no": "7222777"},
        {"bib_no": 85, "licence_no": "7223406"},
        {"bib_no": 86, "licence_no": "722370"},
        {"bib_no": 87, "licence_no": "7224166"},
        {"bib_no": 88, "licence_no": "7225053"},
        {"bib_no": 89, "licence_no": "7225133"},
        {"bib_no": 90, "licence_no": "7225209"},
        {"bib_no": 91, "licence_no": "7304768"},
        {"bib_no": 92, "licence_no": "7513392"},
        {"bib_no": 93, "licence_no": "7525173"},
        {"bib_no": 94, "licence_no": "7730666"},
        {"bib_no": 95, "licence_no": "7752739"},
        {"bib_no": 96, "licence_no": "7762850"},
        {"bib_no": 97, "licence_no": "7791617"},
        {"bib_no": 98, "licence_no": "7895591"},
        {"bib_no": 99, "licence_no": "8049670"},
        {"bib_no": 100, "licence_no": "8079104"},
        {"bib_no": 101, "licence_no": "8226464"},
        {"bib_no": 102, "licence_no": "8261029"},
        {"bib_no": 103, "licence_no": "8274450"},
        {"bib_no": 104, "licence_no": "8310265"},
        {"bib_no": 105, "licence_no": "8526337"},
        {"bib_no": 106, "licence_no": "8546052"},
        {"bib_no": 107, "licence_no": "8552240"},
        {"bib_no": 108, "licence_no": "8560220"},
        {"bib_no": 109, "licence_no": "8618608"},
        {"bib_no": 110, "licence_no": "8875095"},
        {"bib_no": 111, "licence_no": "8981228"},
        {"bib_no": 112, "licence_no": "8987595"},
        {"bib_no": 113, "licence_no": "9239990"},
        {"bib_no": 114, "licence_no": "9240480"},
        {"bib_no": 115, "licence_no": "9240534"},
        {"bib_no": 116, "licence_no": "9245676"},
        {"bib_no": 117, "licence_no": "9256721"},
        {"bib_no": 118, "licence_no": "9257964"},
        {"bib_no": 119, "licence_no": "9321954"},
        {"bib_no": 120, "licence_no": "9321971"},
        {"bib_no": 121, "licence_no": "9322263"},
        {"bib_no": 122, "licence_no": "9323439"},
        {"bib_no": 123, "licence_no": "9324241"},
        {"bib_no": 124, "licence_no": "9424947"},
        {"bib_no": 125, "licence_no": "9510214"},
        {"bib_no": 126, "licence_no": "9523898"},
        {"bib_no": 127, "licence_no": "9538603"},
        {"bib_no": 128, "licence_no": "9621153"},
        {"bib_no": 129, "licence_no": "9720366"},
        {"bib_no": 130, "licence_no": "9861370"},
        {"bib_no": 131, "licence_no": "2814398"},
        {"bib_no": 132, "licence_no": "3525635"},
        {"bib_no": 133, "licence_no": "3712439"},
        {"bib_no": 134, "licence_no": "3714960"},
        {"bib_no": 135, "licence_no": "3726270"},
        {"bib_no": 136, "licence_no": "3727700"},
        {"bib_no": 137, "licence_no": "3727799"},
        {"bib_no": 138, "licence_no": "3731597"},
        {"bib_no": 139, "licence_no": "3731932"},
        {"bib_no": 140, "licence_no": "4111546"},
        {"bib_no": 141, "licence_no": "4422906"},
        {"bib_no": 142, "licence_no": "4435747"},
        {"bib_no": 143, "licence_no": "4451551"},
        {"bib_no": 144, "licence_no": "4462320"},
        {"bib_no": 145, "licence_no": "4519318"},
        {"bib_no": 146, "licence_no": "4526124"},
        {"bib_no": 147, "licence_no": "4527177"},
        {"bib_no": 148, "licence_no": "4527511"},
        {"bib_no": 149, "licence_no": "4529851"},
        {"bib_no": 150, "licence_no": "4532589"},
        {"bib_no": 151, "licence_no": "4935234"},
        {"bib_no": 152, "licence_no": "4939159"},
        {"bib_no": 153, "licence_no": "5324235"},
        {"bib_no": 154, "licence_no": "5324871"},
        {"bib_no": 155, "licence_no": "5325321"},
        {"bib_no": 156, "licence_no": "5326002"},
        {"bib_no": 157, "licence_no": "5326543"},
        {"bib_no": 158, "licence_no": "5327528"},
        {"bib_no": 159, "licence_no": "5327901"},
        {"bib_no": 160, "licence_no": "7213526"},
        {"bib_no": 161, "licence_no": "7217048"},
        {"bib_no": 162, "licence_no": "7217573"},
        {"bib_no": 163, "licence_no": "7219370"},
        {"bib_no": 164, "licence_no": "7219491"},
        {"bib_no": 165, "licence_no": "723342"},
        {"bib_no": 166, "licence_no": "725492"},
        {"bib_no": 167, "licence_no": "7512693"},
        {"bib_no": 168, "licence_no": "7874062"},
        {"bib_no": 169, "licence_no": "7884741"},
        {"bib_no": 170, "licence_no": "9137160"},
        {"bib_no": 171, "licence_no": "9145837"},
        {"bib_no": 172, "licence_no": "9221871"},
        {"bib_no": 173, "licence_no": "9241901"},
        {"bib_no": 174, "licence_no": "9247952"},
        {"bib_no": 175, "licence_no": "9256846"},
        {"bib_no": 176, "licence_no": "9311764"},
        {"bib_no": 177, "licence_no": "1425307"},
        {"bib_no": 178, "licence_no": "3657472"},
        {"bib_no": 179, "licence_no": "3740714"},
        {"bib_no": 180, "licence_no": "4110308"},
        {"bib_no": 181, "licence_no": "4529838"},
        {"bib_no": 182, "licence_no": "5978142"},
        {"bib_no": 183, "licence_no": "6200265"},
        {"bib_no": 184, "licence_no": "6263848"},
        {"bib_no": 185, "licence_no": "7172577"},
        {"bib_no": 186, "licence_no": "7216648"},
        {"bib_no": 187, "licence_no": "7222110"},
        {"bib_no": 188, "licence_no": "7527624"},
        {"bib_no": 189, "licence_no": "7705417"},
        {"bib_no": 190, "licence_no": "798720"},
        {"bib_no": 191, "licence_no": "9036991"},
        {"bib_no": 192, "licence_no": "9536504"},
        {"bib_no": 193, "licence_no": "1420954"},
        {"bib_no": 194, "licence_no": "4528713"},
        {"bib_no": 195, "licence_no": "4529053"},
        {"bib_no": 196, "licence_no": "5327437"},
        {"bib_no": 197, "licence_no": "7223032"},
        {"bib_no": 198, "licence_no": "7224029"},
        {"bib_no": 199, "licence_no": "7886249"},
        {"bib_no": 200, "licence_no": "7887928"},
        {"bib_no": 201, "licence_no": "9242977"},
        {"bib_no": 202, "licence_no": "9252435"},
        {"bib_no": 203, "licence_no": "9321828"},
        {"bib_no": 204, "licence_no": "9426636"},
        {"bib_no": 205, "licence_no": "1383148"},
        {"bib_no": 206, "licence_no": "1614653"},
        {"bib_no": 207, "licence_no": "2198079"},
        {"bib_no": 208, "licence_no": "2885953"},
        {"bib_no": 209, "licence_no": "3180538"},
        {"bib_no": 210, "licence_no": "3211177"},
        {"bib_no": 211, "licence_no": "3447657"},
        {"bib_no": 212, "licence_no": "3537537"},
        {"bib_no": 213, "licence_no": "3761891"},
        {"bib_no": 214, "licence_no": "4427928"},
        {"bib_no": 215, "licence_no": "4455748"},
        {"bib_no": 216, "licence_no": "4472504"},
        {"bib_no": 217, "licence_no": "4526611"},
        {"bib_no": 218, "licence_no": "4877323"},
        {"bib_no": 219, "licence_no": "5318378"},
        {"bib_no": 220, "licence_no": "5324922"},
        {"bib_no": 221, "licence_no": "5325044"},
        {"bib_no": 222, "licence_no": "5325506"},
        {"bib_no": 223, "licence_no": "5325784"},
        {"bib_no": 224, "licence_no": "5325867"},
        {"bib_no": 225, "licence_no": "5327556"},
        {"bib_no": 226, "licence_no": "5477766"},
        {"bib_no": 227, "licence_no": "5615415"},
        {"bib_no": 228, "licence_no": "5953737"},
        {"bib_no": 229, "licence_no": "6021038"},
        {"bib_no": 230, "licence_no": "6021265"},
        {"bib_no": 231, "licence_no": "608834"},
        {"bib_no": 232, "licence_no": "61624"},
        {"bib_no": 233, "licence_no": "6448793"},
        {"bib_no": 234, "licence_no": "7037313"},
        {"bib_no": 235, "licence_no": "7214582"},
        {"bib_no": 236, "licence_no": "7218004"},
        {"bib_no": 237, "licence_no": "7221154"},
        {"bib_no": 238, "licence_no": "7221254"},
        {"bib_no": 239, "licence_no": "7545339"},
        {"bib_no": 240, "licence_no": "8341640"},
        {"bib_no": 241, "licence_no": "8393682"},
        {"bib_no": 242, "licence_no": "8559774"},
        {"bib_no": 243, "licence_no": "8960031"},
        {"bib_no": 244, "licence_no": "9143724"},
        {"bib_no": 245, "licence_no": "9457149"},
        {"bib_no": 246, "licence_no": "9509020"},
        {"bib_no": 247, "licence_no": "9532616"},
        {"bib_no": 248, "licence_no": "9943272"},
        {"bib_no": 249, "licence_no": "7220549"},
        {"bib_no": 250, "licence_no": "7731399"},
        {"bib_no": 251, "licence_no": "914291"},
        {"bib_no": 252, "licence_no": "9410780"},
        {"bib_no": 253, "licence_no": "1139461"},
        {"bib_no": 254, "licence_no": "1180036"},
        {"bib_no": 255, "licence_no": "1469002"},
        {"bib_no": 256, "licence_no": "1633220"},
        {"bib_no": 257, "licence_no": "1839508"},
        {"bib_no": 258, "licence_no": "2610171"},
        {"bib_no": 259, "licence_no": "2772999"},
        {"bib_no": 260, "licence_no": "2861042"},
        {"bib_no": 261, "licence_no": "2885295"},
        {"bib_no": 262, "licence_no": "2962968"},
        {"bib_no": 263, "licence_no": "3054167"},
        {"bib_no": 264, "licence_no": "3109349"},
        {"bib_no": 265, "licence_no": "3479829"},
        {"bib_no": 266, "licence_no": "3520070"},
        {"bib_no": 267, "licence_no": "3524722"},
        {"bib_no": 268, "licence_no": "3639845"},
        {"bib_no": 269, "licence_no": "3689010"},
        {"bib_no": 270, "licence_no": "3851469"},
        {"bib_no": 271, "licence_no": "3942567"},
        {"bib_no": 272, "licence_no": "3993245"},
        {"bib_no": 273, "licence_no": "4075778"},
        {"bib_no": 274, "licence_no": "4351041"},
        {"bib_no": 275, "licence_no": "4498625"},
        {"bib_no": 276, "licence_no": "4550428"},
        {"bib_no": 277, "licence_no": "4583122"},
        {"bib_no": 278, "licence_no": "4741343"},
        {"bib_no": 279, "licence_no": "4927421"},
        {"bib_no": 280, "licence_no": "5115500"},
        {"bib_no": 281, "licence_no": "5253488"},
        {"bib_no": 282, "licence_no": "5406735"},
        {"bib_no": 283, "licence_no": "5415460"},
        {"bib_no": 284, "licence_no": "5644426"},
        {"bib_no": 285, "licence_no": "5645921"},
        {"bib_no": 286, "licence_no": "5687004"},
        {"bib_no": 287, "licence_no": "5795431"},
        {"bib_no": 288, "licence_no": "5801493"},
        {"bib_no": 289, "licence_no": "5905725"},
        {"bib_no": 290, "licence_no": "5921885"},
        {"bib_no": 291, "licence_no": "6096680"},
        {"bib_no": 292, "licence_no": "6386380"},
        {"bib_no": 293, "licence_no": "6393985"},
        {"bib_no": 294, "licence_no": "6573403"},
        {"bib_no": 295, "licence_no": "6643354"},
        {"bib_no": 296, "licence_no": "6710253"},
        {"bib_no": 297, "licence_no": "6712951"},
        {"bib_no": 298, "licence_no": "6797769"},
        {"bib_no": 299, "licence_no": "6817758"},
        {"bib_no": 300, "licence_no": "6818455"},
        {"bib_no": 301, "licence_no": "6821111"},
        {"bib_no": 302, "licence_no": "6943635"},
        {"bib_no": 303, "licence_no": "6998380"},
        {"bib_no": 304, "licence_no": "7219456"},
        {"bib_no": 305, "licence_no": "7221275"},
        {"bib_no": 306, "licence_no": "7343060"},
        {"bib_no": 307, "licence_no": "7427783"},
        {"bib_no": 308, "licence_no": "7541332"},
        {"bib_no": 309, "licence_no": "7615510"},
        {"bib_no": 310, "licence_no": "7807813"},
        {"bib_no": 311, "licence_no": "7810196"},
        {"bib_no": 312, "licence_no": "7894402"},
        {"bib_no": 313, "licence_no": "7899094"},
        {"bib_no": 314, "licence_no": "8190556"},
        {"bib_no": 315, "licence_no": "8390927"},
        {"bib_no": 316, "licence_no": "8850402"},
        {"bib_no": 317, "licence_no": "9023117"},
        {"bib_no": 318, "licence_no": "9206653"},
        {"bib_no": 319, "licence_no": "9293868"},
        {"bib_no": 320, "licence_no": "9333796"},
        {"bib_no": 321, "licence_no": "9347676"},
        {"bib_no": 322, "licence_no": "9360148"},
        {"bib_no": 323, "licence_no": "9436650"},
        {"bib_no": 324, "licence_no": "9475596"},
        {"bib_no": 325, "licence_no": "9488140"},
        {"bib_no": 326, "licence_no": "9519526"},
        {"bib_no": 327, "licence_no": "9771755"},
        {"bib_no": 328, "licence_no": "9820260"},
        {"bib_no": 329, "licence_no": "9851412"},
        {"bib_no": 330, "licence_no": "9852847"},
        {"bib_no": 331, "licence_no": "9863345"},
        {"bib_no": 332, "licence_no": "9876018"},
        {"bib_no": 333, "licence_no": "1032773"},
        {"bib_no": 334, "licence_no": "2188188"},
        {"bib_no": 335, "licence_no": "2360911"},
        {"bib_no": 336, "licence_no": "2731770"},
        {"bib_no": 337, "licence_no": "5787220"},
        {"bib_no": 338, "licence_no": "6842715"},
        {"bib_no": 339, "licence_no": "7210055"},
        {"bib_no": 340, "licence_no": "1689719"},
        {"bib_no": 341, "licence_no": "3702448"},
        {"bib_no": 342, "licence_no": "4415078"},
        {"bib_no": 343, "licence_no": "4932894"},
        {"bib_no": 344, "licence_no": "5189163"},
        {"bib_no": 345, "licence_no": "7221748"},
    ],
}


already_set_bib_nos = {"licenceNos": ["5325506", "722370"]}


class TestAPIAssignAllBibNos(BaseTest):
    def test_correct_assign_all(self, admin_client, reset_db, populate):
        with freeze_time(after_cutoff):
            r = admin_client.post("/api/admin/bibs")
            assert r.status_code == HTTPStatus.OK, r.json
            assert r.json == correct_admin_assign_all_response, r.json

    def test_incorrect_assign_all_already_set(
        self,
        admin_client,
        reset_db,
        populate,
        set_a_few_bibs,
    ):
        error = ae.BibConflictError(
            origin=origin,
            error_message=ae.SOME_BIBS_ALREADY_ASSIGNED_MESSAGE,
            payload=already_set_bib_nos,
        )
        with freeze_time(after_cutoff):
            r = admin_client.post("/api/admin/bibs")
            assert r.status_code == error.status_code, r.json
            assert r.json == error.to_dict(), r.json

    def test_incorrect_assign_before_cutoff(self, admin_client, reset_db, populate):
        error = ae.RegistrationCutoffError(
            origin=origin,
            error_message=ae.REGISTRATION_MESSAGES["not_ended"],
        )
        with freeze_time(before_cutoff):
            r = admin_client.post("/api/admin/bibs")
            assert r.status_code == error.status_code, r.json
            assert r.json == error.to_dict(), r.json
